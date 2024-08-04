""" Information about my emergency fund """

import streamlit as st
import plotly.express as px
from utils import data_prep

st.write("# Emergency Fund 🔥")

exclude = ['Regular Saver', 'Marcus']
page_cash_accounts = list(set(data_prep.CASH_ACCOUNTS).difference(set(exclude)))

df = data_prep.load_account_data(exclude=exclude)
month_now, month_previous = data_prep.calc_date_indices()

FUND = 6000
cash = df.loc[month_now, 'Total Cash']

st.write((
    f'Your emergency fund is set to: **£{FUND:,.2f}**, which gives you £{FUND/3:,.2f}'
    ' per month for 3 months if something bad happens...'
))
st.write(f"Cash accounts: {', '.join(page_cash_accounts)}")

if cash >= FUND:
    HLINE_COL = 'green'
    message = (
        'You have enough cash to cover your emergency fund'
        f', with **£{cash-FUND:,.2f}** on top!'
    )
else:
    HLINE_COL = 'red'
    message = (
        'You do not have enough cash to cover your emergency fund'
        f"; you're missing **£{FUND-cash:,.2f}**"
    )

# Available cash plot
fig1 = px.line(df['Total Cash'],
              labels={
                  "value": "Amount (£)",
                  "Date": ""
              },
              title="Available Cash",
              color_discrete_sequence=['lightgreen'])
fig1.add_hline(y=FUND, line_dash="dash", line_color=HLINE_COL)
fig1.add_hrect(y0=0, y1=FUND, line_width=0, fillcolor=HLINE_COL, opacity=0.2)
fig1.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
st.plotly_chart(fig1)

st.write(message)

# Breakdown of cash accounts plot
fig2 = px.bar(df[page_cash_accounts],
              title="How your cash is split")
fig2.add_hline(y=FUND, line_dash="dash")
fig2.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
st.plotly_chart(fig2)

if len(exclude) > 0:
    st.write(f"All figures exclude accounts: {', '.join(exclude)}")
