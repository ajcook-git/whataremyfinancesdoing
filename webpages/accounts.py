""" Accounts data """

import streamlit as st
import plotly.express as px

from utils import data_prep

df = data_prep.load_account_data()

st.write("# Accounts 🏦")

st.write("### Cash")
fig1 = px.line(df[data_prep.CASH_ACCOUNTS], labels={"value": "Amount (£)", "Date": ""})
fig1.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
st.plotly_chart(fig1)

st.write("### Investment")
fig3 = px.line(df[data_prep.INVESTMENT_ACCOUNTS], labels={"value": "Amount (£)", "Date": ""})
fig3.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
st.plotly_chart(fig3)

st.divider()

st.write("""### Credit
This represents the amount of debt currently on Credit Cards.
""")
fig2 = px.line(df[data_prep.CREDIT_ACCOUNTS], labels={"value": "Amount (£)", "Date": ""})
fig2.add_hline(y=12000, line_dash='dash', annotation={'text': 'Combined credit limit'})
fig2.add_hline(y=5500, line_dash='dash', annotation={'text': 'Natwest credit climit'})
fig2.add_hline(y=6500, line_dash='dash', annotation={'text': 'Barclays credit limit'})
fig2.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
st.plotly_chart(fig2)
