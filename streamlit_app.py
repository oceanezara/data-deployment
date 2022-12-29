import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go

from plotly.subplots import make_subplots



DATA = "get_around_delay_analysis.xlsx"

@st.cache
def load_data():
    data = pd.read_excel(DATA)
    return data



data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("")

#dataset where time_delta_with_previous_rental_in_minutes is not null

df_delta_not_null = data[data['time_delta_with_previous_rental_in_minutes'].notnull()]
df_delta_not_null.head()

#ratio en % des type de location
ratio_checking_type = data["checkin_type"].value_counts(normalize=True)

ratio_state = data["state"].value_counts(normalize=True).round(3)

# ratio d'annulation selon type de location
mobile = data[data["checkin_type"] == "mobile"]
mobile_ratio_state = mobile["state"].value_counts(normalize=True).round(3)

connect = data[data["checkin_type"] == "connect"]
connect_ratio_state = connect["state"].value_counts(normalize=True).round(3)

# new dataFrame incluant que les retards
data_retard = data[data["previous_ended_rental_id"] != "NaN"]

data_mobile = data_retard[data_retard["checkin_type"] == "mobile"]
retard_mobil = data_mobile["delay_at_checkout_in_minutes"].mean()

data_connect = data_retard[data_retard["checkin_type"] == "connect"]
retard_connect = data_connect["delay_at_checkout_in_minutes"].mean()

# histogramme
histo_checkout = data[(data["delay_at_checkout_in_minutes"] > -1440) & (data["delay_at_checkout_in_minutes"] < 1440)]
histo_delta = data[(data["time_delta_with_previous_rental_in_minutes"] > -1440) & (data["time_delta_with_previous_rental_in_minutes"] < 1440)]





st.markdown("<h1 style='text-align: center; color: white;'>Dashbord GetAround</h1>", unsafe_allow_html=True)
st.markdown("###")

pie = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]],shared_yaxes = True, 
                    x_title="proportion des type de location et % d'annulation",
                    subplot_titles=["Distribution de type de location", "proportion des annulation"])

pie.add_trace(go.Pie( 
    values=ratio_checking_type,
    labels=['Mobile', 'Connect '],
    marker_colors = ['#202EBD','#13E7E3'],                      
    ),
    row=1, col=1)

pie.add_trace(go.Pie(
    values=ratio_state,
    labels=['Non annulée', 'Annulée '],
    marker_colors = ['#20BD2E','#FF3333'],
    ),
    row=1, col=2)

pie.update_layout(
    width=1200,
    legend=dict(
        font=dict(
            size=16
        )))

st.plotly_chart(pie)

fig_pie = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]],shared_yaxes = True,
                        x_title='proportion des annulation par type de location',subplot_titles=["Mobile", "Connect"])

fig_pie.add_trace(go.Pie( 
    values=mobile_ratio_state,
    labels=['Non annulée', 'Annulée'],
    marker_colors = ['#20BD2E','#FF3333'],                      
    ),
    row=1, col=1)

fig_pie.add_trace(go.Pie(
    values=connect_ratio_state,
    labels=['Non annulée', 'Annulée'],
    marker_colors = ['#20BD2E','#FF3333'],
    ),
    row=1, col=2)

fig_pie.update_layout(
    width=1200,
    legend=dict(
        font=dict(
            size=16
        )))

st.plotly_chart(fig_pie)

st.markdown("###")

st.write(f'Le retard moyen pour la version mobil est de {round(retard_mobil)} minutes')

st.write(f'Le retard moyen pour la version connect est de {round(retard_connect)} minutes')


fig = px.histogram(histo_delta, x="time_delta_with_previous_rental_in_minutes",
                      title = 'histogramme sur 24 heures',
                      color = 'checkin_type',
                      barmode ='group',
                      width= 1200,
                      height = 600
                      ) 
fig.update_layout(title_x = 0.5,
                    legend=dict(
                        font=dict(
                    size=16
                    ))) 
                            
st.plotly_chart(fig)

fig = px.histogram(histo_checkout, x="delay_at_checkout_in_minutes",
                      title = 'histogramme sur 24 heures',
                      color = 'checkin_type',
                      barmode ='group',
                      width= 1200,
                      height = 600
                      ) 
fig.update_layout(title_x = 0.5,
                legend=dict(
                    font=dict(
                size=16
                ))) 
      
st.plotly_chart(fig)