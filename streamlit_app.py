import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Adam's finances
This is a dashboard for Adam. Yes, I know it's public.
"""

df = pd.read_csv('data/newdata.csv', index_col='Date')

credit_cols = {'Barclaycard', 'NatwestCredit'}
debit_cols = list(set(df.columns).difference(credit_cols))

st.line_chart(df[debit_cols])

st.dataframe(df)
