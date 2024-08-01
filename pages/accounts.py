""" Accounts data """

import streamlit as st
import plotly.express as px

from utils import data_prep

df = data_prep.load_account_data()

st.write("# Accounts")
debit_fig = px.line(df[data_prep.CURRENT_ACCOUNTS_DESC], labels=dict(value='Amount (£)', Date=""),
    title="Current value of accounts over time")
debit_fig.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
# debit_fig.update_layout(legend=dict(orientation='h', y=-0.3, yanchor='auto',),
#                         legend_title=dict(text=None))
st.plotly_chart(debit_fig)
