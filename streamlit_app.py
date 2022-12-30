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







# #ratio en % des type de location
# ratio_checking_type = data["checkin_type"].value_counts(normalize=True)

# ratio_state = data["state"].value_counts(normalize=True).round(3)

# # ratio d'annulation selon type de location
# mobile = data[data["checkin_type"] == "mobile"]
# mobile_ratio_state = mobile["state"].value_counts(normalize=True).round(3)

# connect = data[data["checkin_type"] == "connect"]
# connect_ratio_state = connect["state"].value_counts(normalize=True).round(3)

# # new dataFrame incluant que les retards
# data_retard = data[data["previous_ended_rental_id"] != "NaN"]

# data_mobile = data_retard[data_retard["checkin_type"] == "mobile"]
# retard_mobil = data_mobile["delay_at_checkout_in_minutes"].mean()

# data_connect = data_retard[data_retard["checkin_type"] == "connect"]
# retard_connect = data_connect["delay_at_checkout_in_minutes"].mean()



# st.markdown("<h1 style='text-align: center; color: white;'>Dashbord GetAround</h1>", unsafe_allow_html=True)
# st.markdown("###")

# pie = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]],shared_yaxes = True, 
#                     x_title="proportion des type de location et % d'annulation",
#                     subplot_titles=["Distribution de type de location", "proportion des annulation"])

# pie.add_trace(go.Pie( 
#     values=ratio_checking_type,
#     labels=['Mobile', 'Connect '],
#     marker_colors = ['#202EBD','#13E7E3'],                      
#     ),
#     row=1, col=1)

# pie.add_trace(go.Pie(
#     values=ratio_state,
#     labels=['Non annulée', 'Annulée '],
#     marker_colors = ['#20BD2E','#FF3333'],
#     ),
#     row=1, col=2)

# pie.update_layout(
#     width=1200,
#     legend=dict(
#         font=dict(
#             size=16
#         )))

# st.plotly_chart(pie)

# fig_pie = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]],shared_yaxes = True,
#                         x_title='proportion des annulation par type de location',subplot_titles=["Mobile", "Connect"])

# fig_pie.add_trace(go.Pie( 
#     values=mobile_ratio_state,
#     labels=['Non annulée', 'Annulée'],
#     marker_colors = ['#20BD2E','#FF3333'],                      
#     ),
#     row=1, col=1)

# fig_pie.add_trace(go.Pie(
#     values=connect_ratio_state,
#     labels=['Non annulée', 'Annulée'],
#     marker_colors = ['#20BD2E','#FF3333'],
#     ),
#     row=1, col=2)

# fig_pie.update_layout(
#     width=1200,
#     legend=dict(
#         font=dict(
#             size=16
#         )))

# st.plotly_chart(fig_pie)

# st.markdown("###")

# st.write(f'Le retard moyen pour la version mobil est de {round(retard_mobil)} minutes')

# st.write(f'Le retard moyen pour la version connect est de {round(retard_connect)} minutes')




