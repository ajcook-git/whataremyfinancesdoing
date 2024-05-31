# import altair as alt
# import numpy as np
import datetime
import pandas as pd
# import plotly.express as px
import streamlit as st
import textwrap

"""
# Adam's finances
This is a dashboard for Adam. Yes, I know it's public.
"""

df = pd.read_csv('data/newdata.csv', index_col='Date')

if all(df.iloc[datetime.datetime.now().month].notna()):
    st.write(textwrap.dedent("""
        *Warning:* it looks like your data is out of date!
    """))

credit_accs = {'Barclaycard', 'NatwestCredit'}
credit_cols = list(credit_accs)
debit_accs = set(df.columns).difference(credit_cols)
debit_cols = list(debit_accs)

debit_df = df[debit_cols]
debit_df['Total'] = debit_df.transpose().sum()
credit_df = df[credit_cols]
credit_df['Total'] = credit_df.transpose().sum()

st.write("### These lines represent actual cash")
st.line_chart(debit_df)

st.write("### These lines represent credit card debt")
st.line_chart(credit_df)

st.write("### Here's the raw data I'm reading from")
st.dataframe(df)
