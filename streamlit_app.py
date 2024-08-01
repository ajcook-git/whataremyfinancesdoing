"""
This application is for showing my current finances, in pretty graphs.

"""

import datetime
import streamlit as st

st.set_page_config(page_title="Finances", page_icon=":material/paid:")

summary = st.Page("pages/summary.py", title="Summary", icon=":material/home:")
accounts = st.Page("pages/accounts.py", title="Accounts", icon=":material/account_balance:")
todo = st.Page("pages/todo.py", title="To-do", icon=":material/checklist:")

container = st.sidebar.container()
container.write(f"{datetime.datetime.now().strftime('%A %d %B, %Y')}")

pg = st.navigation([summary, accounts, todo])
pg.run()
