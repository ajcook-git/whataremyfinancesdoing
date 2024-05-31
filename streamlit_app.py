import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Adam's finances
This is a dashboard for Adam. Yes, I know it's public.
"""

df = pd.read_csv('data/newdata.csv', index_col='Date')

st.dataframe(df)
