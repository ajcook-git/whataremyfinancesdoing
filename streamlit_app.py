"""
This application is for showing my current finances, in pretty graphs.

"""

import datetime
import textwrap
import plotly.express as px
import streamlit as st
import data_prep

st.set_page_config(page_title="Finances", page_icon="💵")

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

def create_totals():
    """ Create totals container """

    with st.container(border=True):
        st.write(f"Taking into account data up to {datetime.datetime.strptime(month_now, '%Y-%m').strftime('%B')}")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total in Accounts", f"£{ACC_NOW:,.2f}", f"{ACC_NOW-ACC_PREVIOUS:,.2f}")
        col2.metric("Total in Credit", f"£{CREDIT_NOW:,.2f}", f"{CREDIT_NOW-CREDIT_PREVIOUS:,.2f}",
                    delta_color='inverse')
        col3.metric("Total Net", f"£{NET_NOW:,.2f}", f"{NET_NOW-NET_PREVIOUS:,.2f}")

st.markdown(f"""
# Finances
**{datetime.datetime.now().strftime('%A %d %B, %Y')}**
""")

if not all(df.loc[month_now].notna()):
    st.write(textwrap.dedent("""
        **Warning:** it looks like your data is out of date!
    """))

create_totals()

summary, acc_tab, credit_tab, creditscore_tab, todo_tab = st.tabs(
    ['Summary', 'Accounts', 'Credit', 'Credit Scores', 'To do'])

with summary:
    if NET_NOW - NET_PREVIOUS >= 0:
        HOME_MESSAGE = "Your finances are looking :green[good]! 💸"
    else:
        HOME_MESSAGE = "Your finances went :red[down] this month."
        if NET_NOW >= 0:
            HOME_MESSAGE += " But overall, you're still :green[positive]! 😀"
    st.write(f"### Summary\n{HOME_MESSAGE}")
    totals_fig = px.line(df[['AccTotals', 'CredTotals', 'NetTotals']],
                        labels=dict(value='Amount (£)', Date=""),
                        title="Total in Accounts, and on Credit Card",
                        color_discrete_sequence=['lightgreen', 'tomato', 'darkslategray'])
    totals_fig.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
    st.plotly_chart(totals_fig)

with acc_tab:
    st.write("### Account Balance")
    debit_fig = px.line(df[data_prep.CURRENT_ACCOUNTS_DESC], labels=dict(value='Amount (£)', Date=""),
        title="Current value of accounts over time")
    debit_fig.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
    # debit_fig.update_layout(legend=dict(orientation='h', y=-0.3, yanchor='auto',),
    #                         legend_title=dict(text=None))
    st.plotly_chart(debit_fig)

with credit_tab:
    pass
    # st.write("### Credit Card Balance")
    # credit_fig = px.line(credit_df, labels=dict(value='Amount (£)', Date=""))
    # credit_fig.update_xaxes(dtick="M1", tickformat="%b\n%Y", ticklabelmode="period")
    # credit_fig.update_layout(legend=dict(orientation='h', y=-0.3, yanchor='auto', ),
    #                          legend_title=dict(text=None))
    # st.plotly_chart(credit_fig)

with creditscore_tab:
    pass
    # I use 3 providers to access all three brokers' scores in the UK:
    # - Experian = Experian (score/999)
    # - Equifax = Clear Score (score/1000)
    # - TransUnion = Credit Karma (score/710)
    # month_now = datetime.datetime.now().strftime('%Y-%m')
    # mask = [999, 1_000, 710]

    # # data = csdf.loc[month_now, 'Equifax'] / 999

    # fig = px.pie()
    # st.plotly_chart(fig)

with todo_tab:
    things_to_do = textwrap.dedent("""
        - Improve hover data on existing graphs
        - Add information about Credit Scores
        - Add totals to existing graphs
        - Combined debit and credit graph(s)
        - Breakdown of spending
        - (link to Monzo) - hightlight trends and recent transactions?
        - Show personal allocation between banks
        - Track inflation and the BoE base rate
        - Track savings interest per account, and interest on Credit cards
        - Create personal CPI for products tailored to me
        - Track emergency fund
        - Track local property value 
        - Show amount invested vs. cash vs. credit
    """)
    st.write(f"""
    ### Summary of ideas to implement next
    {things_to_do}
    """)
