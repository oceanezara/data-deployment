import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots


### Config
st.set_page_config(
    page_title="GetAround Delay",
    page_icon=':blue_car:',
)
DATA = "get_around_delay_analysis.xlsx"

@st.cache
def load_data():
    data = pd.read_excel(DATA)
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("")

st.header('GetAround Delay Analysis Dashboard :blue_car:')

st.subheader(
    '1) Data description'
)
st.write('')

st.write('**Data head :**')
st.write(data.head())
st.markdown("***")
st.write('**Number of rows :** ', data.shape[0])
st.markdown("***")
st.write('**Percentage of missing values :** ')
st.write(100*data.isnull().sum()/data.shape[0])


#dataset where time_delta_with_previous_rental_in_minutes is not null


# I replace NaN values at column delay_at_checkout_in_minutes by zero when state is ended 
mask = (data['state'] == 'ended') 
data['delay_at_checkout_in_minutes'] = data[mask]['delay_at_checkout_in_minutes'].fillna(0)

# Mean per checking type
st.markdown("***")
st.write('**Average delay per checking type in minutes :**')
mean_per_checking_type = data.groupby(['checkin_type'])['delay_at_checkout_in_minutes'].mean()
st.write(mean_per_checking_type)

avg_checking_type_df = data.groupby(['checkin_type']).mean()

bar_fig = plt.figure(figsize=(8,7))

bar_ax = bar_fig.add_subplot(111)

sub_avg_breast_cancer_df = avg_checking_type_df[["delay_at_checkout_in_minutes"]]

sub_avg_breast_cancer_df.plot.bar(alpha=0.8, ax=bar_ax, )
st.pyplot(bar_fig)

st.markdown("***")
st.write('**Type of cars and state of booking distributions:**')


pie = make_subplots(rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]],shared_yaxes = True, 
                    subplot_titles=["Type of cars", "State of booking"])

pie.add_trace(go.Pie( 
    values=data['checkin_type'].value_counts(normalize=True),
    labels=data['checkin_type'].value_counts(normalize=True).index,
    marker_colors = ['#202EBD','#13E7E3'],                      
    ),
    row=1, col=1)

pie.add_trace(go.Pie(
    values=data["state"].value_counts(normalize=True).round(3),
    labels=data['state'].value_counts(normalize=True).index,
    marker_colors = ['#20BD2E','#FF3333'],
    ),
    row=1, col=2)
pie.update_traces(hole=.4, textinfo="label+percent")    

pie.update_layout(
    width=1200,
    legend=dict(
        font=dict(
            size=16
        )))

st.plotly_chart(pie)

st.subheader(
    '2) Data cleaning'
)
st.write('')
st.write("Let's remove all entries where time_delta_with_previous_rental_in_minutes is NaN as it corresponds to a delta greater than 12 hours")

#dataset where time_delta_with_previous_rental_in_minutes is not null

data_delta_not_null = data[data['time_delta_with_previous_rental_in_minutes'].notnull()]

st.write(data_delta_not_null['checkin_type'].value_counts())

st.write("Now we will be working on ", data_delta_not_null.shape[0], "rows")

st.markdown("***")
st.write('**Proportion of cancelation per type of check in :** ')
st.write()

# ratio d'annulation selon type de location
mobile = data_delta_not_null[data_delta_not_null["checkin_type"] == "mobile"]
mobile_ratio_state = mobile["state"].value_counts(normalize=True).round(3)

connect = data_delta_not_null[data_delta_not_null["checkin_type"] == "connect"]
connect_ratio_state = connect["state"].value_counts(normalize=True).round(3)

fig_pie = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]],shared_yaxes = True,
subplot_titles=["Mobile", "Connect"])

fig_pie.add_trace(go.Pie( 
    values=mobile_ratio_state,
    labels=['Ended', 'Canceled'],
    marker_colors = ['#20BD2E','#FF3333'],                      
    ),
    row=1, col=1)

fig_pie.add_trace(go.Pie(
    values=connect_ratio_state,
    labels=['Ended', 'Canceled'],
    marker_colors = ['#20BD2E','#FF3333'],
    ),
    row=1, col=2)
fig_pie.update_traces(hole=.4, textinfo="label+percent")   

fig_pie.update_layout(
    width=1200,
    legend=dict(
        font=dict(
            size=16
        )))

st.plotly_chart(fig_pie)

st.write(data_delta_not_null.groupby(['checkin_type', 'state'])['time_delta_with_previous_rental_in_minutes'].describe())

st.markdown("***")
st.write('**Which share of our owner’s revenue would potentially be affected by the feature How many rentals would be affected by the feature depending on the threshold and scope we choose?**')

threshold = st.select_slider('Choose a threshold on Connect feature only: ', options=[60, 240, 570, 720])

data_delta_not_null_new = data_delta_not_null.drop(data_delta_not_null[(data_delta_not_null['checkin_type'] == 'connect') & (data_delta_not_null['time_delta_with_previous_rental_in_minutes'] <= threshold)].index)

st.write(data_delta_not_null_new.groupby(['checkin_type', 'state'])['time_delta_with_previous_rental_in_minutes'].describe())

mask_connect = data_delta_not_null['checkin_type'] == 'connect'
mask_ended = data_delta_not_null['state'] == 'ended'
mask_connect_new = data_delta_not_null_new['checkin_type'] == 'connect'
mask_ended_new = data_delta_not_null_new['state'] == 'ended'


diff = data_delta_not_null[mask_connect & mask_ended]['state'].count() - data_delta_not_null_new[mask_connect_new & mask_ended_new]['state'].count()

st.write('It will potentially affect ', ((diff/data.shape[0])*100).round(2), "% of owner's revenue")









