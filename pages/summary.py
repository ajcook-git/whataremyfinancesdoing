""" Summary page """

import datetime
import textwrap
import plotly.express as px
import streamlit as st

from utils import data_prep

# load data
df = data_prep.load_account_data(exclude=['Marcus'])
credit_df = data_prep.load_creditscores()

def _calc_date_indices() -> tuple[str]:
    """ Get values for the current and previous month """
    today = datetime.date.today()
    last_month = today.replace(day=1) - datetime.timedelta(days=1)

    return today.strftime('%Y-%m'), last_month.strftime('%Y-%m')

month_now, month_previous = _calc_date_indices()
ACC_NOW = df.loc[month_now, 'AccTotals']
ACC_PREVIOUS = df.loc[month_previous, 'AccTotals']
CREDIT_NOW = df.loc[month_now, 'CredTotals']
CREDIT_PREVIOUS = df.loc[month_previous, 'CredTotals']

NET_NOW = df.loc[month_now, 'NetTotals']
NET_PREVIOUS = df.loc[month_previous, 'NetTotals']

st.write("# Summary")

if not all(df.loc[month_now].notna()):
    st.write(textwrap.dedent("""
        **Warning:** it looks like your data is out of date!
    """))

col1, col2, col3 = st.columns(3)
col1.metric("Total in Accounts", f"£{ACC_NOW:,.2f}", f"{ACC_NOW-ACC_PREVIOUS:,.2f}")
col2.metric("Total in Credit", f"£{CREDIT_NOW:,.2f}", f"{CREDIT_NOW-CREDIT_PREVIOUS:,.2f}",
            delta_color='inverse')
col3.metric("Total Net", f"£{NET_NOW:,.2f}", f"{NET_NOW-NET_PREVIOUS:,.2f}")

totals_fig = px.line(df[['AccTotals', 'CredTotals', 'NetTotals']],
                    labels=dict(
                        value='Amount (£)',
                        Date="",
                        AccTotals="Accounts",
                        CredTotals="Credit",
                        NetTotals="Net"
                    ),
                    title="Total in Accounts, and on Credit Card",
                    color_discrete_sequence=['lightgreen', 'tomato', 'darkslategray'])
totals_fig.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
st.plotly_chart(totals_fig)


