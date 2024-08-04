""" Summary page """

import plotly.express as px
import streamlit as st

from utils import data_prep

df = data_prep.load_account_data(exclude=['Marcus'])

st.write("# Summary 👁️")

totals = ['Accounts Total', 'Credit Total', 'Net Total']
fig1 = px.line(df[totals],
                    labels={
                        "value": "Amount (£)",
                        "Date": ""
                    },
                    title="Total in Accounts, and on Credit Card",
                    color_discrete_sequence=['lightgreen', 'tomato', 'darkslategray'])
fig1.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
# fig1.update_yaxes(autorange="max", range=[0, 15000])

st.plotly_chart(fig1)
