"""
This application is for showing my current finances, in pretty graphs.

"""

import datetime
import streamlit as st
from utils import data_prep

st.set_page_config(page_title="What's my money doing?", page_icon=":material/paid:")

summary = st.Page("webpages/summary.py", title="Summary", icon=":material/home:")
accounts = st.Page("webpages/accounts.py", title="Accounts", icon=":material/account_balance:")
todo = st.Page("webpages/todo.py", title="To-do", icon=":material/checklist:")
goals = st.Page("webpages/goals.py", title="Goals", icon=":material/target:")
bills = st.Page("webpages/bills.py", title="Bills", icon=":material/receipt_long:")
mortgage = st.Page("webpages/mortgage.py", title="Mortgage", icon=":material/real_estate_agent:")
emergency = st.Page("webpages/emergency_fund.py", title="Emergency Fund",
                    icon=":material/emergency_heat:")
credit_score = st.Page("webpages/credit_scores.py", title="Credit Score",
                       icon=":material/credit_score:")

with st.sidebar.container():
    st.write(f"### {datetime.datetime.now().strftime('%A %d %B, %Y')}")

    df = data_prep.load_account_data(exclude=['Marcus'])

    month_now, month_previous = data_prep.calc_date_indices()
    ACC_NOW = df.loc[month_now, 'Accounts Total']
    ACC_PREVIOUS = df.loc[month_previous, 'Accounts Total']
    CREDIT_NOW = df.loc[month_now, 'Credit Total']
    CREDIT_PREVIOUS = df.loc[month_previous, 'Credit Total']

    NET_NOW = df.loc[month_now, 'Net Total']
    NET_PREVIOUS = df.loc[month_previous, 'Net Total']

    st.metric("Accounts", f"£{ACC_NOW:,.2f}", f"{ACC_NOW-ACC_PREVIOUS:,.2f}")
    st.metric("Credit Card", f"£{CREDIT_NOW:,.2f}", f"{CREDIT_NOW-CREDIT_PREVIOUS:,.2f}",
                delta_color='inverse')
    st.metric("Total Net", f"£{NET_NOW:,.2f}", f"{NET_NOW-NET_PREVIOUS:,.2f}")

pg = st.navigation([summary, accounts, bills, goals, emergency, mortgage,
                    credit_score, todo])
pg.run()
