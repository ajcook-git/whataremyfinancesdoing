import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Adam's finances
This is a dashboard for Adam. Yes, I know it's public.

I feel like this is a really cool thing - Streamlit.
"""

df = pd.read_csv('data/newdata.csv', index_col='Date')

credit_cols = {'Barclaycard', 'NatwestCredit'}
debit_cols = list(set(df.columns).difference(credit_cols))

st.write("## These lines represent actual cash")
st.line_chart(df[debit_cols])

st.write("## These lines represent credit card debt")
st.line_chart(df[debit_cols])

st.write("## Here's the raw data I'm reading from")
st.dataframe(df)
