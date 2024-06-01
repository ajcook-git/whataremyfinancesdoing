import datetime
import pandas as pd
import plotly.express as px
import streamlit as st
import textwrap

st.set_page_config(layout="centered")  # set to "wide" for widescreen

"""
# Adam's Financial Health 💵
Yes, I know it's public.
"""

df = pd.read_csv('data/newdata.csv', index_col='Date')
df.rename({
     'MoneyboxCashISA': 'Cash ISA',
     'MoneyboxS&SISA': 'Stocks/Shares ISA',
     'NatwestSavings': 'Regular Saver',
     'UlsterBank': 'Easy-access Saver',
     'Barclaycard': 'Credit card (primary)',
     'NatwestCredit': 'Credit card (secondary)'
}, axis=1, inplace=True)

if not all(df.iloc[datetime.datetime.now().month-1].notna()):
    st.write(textwrap.dedent("""
        **Warning:** it looks like your data is out of date!
    """))
st.write(f"Today's date: {datetime.datetime.now().strftime('%A %d %B %Y')}")

# Seperate credit and debit accounts
credit_accs = {'Credit card (primary)', 'Credit card (secondary)'}
credit_cols = list(credit_accs)
debit_accs = set(df.columns).difference(credit_cols)
debit_cols = list(debit_accs)
debit_cols.remove("Marcus")

debit_df = df[debit_cols]
# debit_df['Total'] = debit_df.transpose().sum()
credit_df = df[credit_cols]
# credit_df['Total'] = credit_df.transpose().sum()

st.write("### Summary")
with st.container():
    col1, col2, col3 = st.columns(3)
    month_now = datetime.datetime.now().month - 1
    month_last = month_now - 1
    with col1:
        total1 = debit_df.iloc[month_now].sum()
        st.metric("Debit", f"£{total1:,.2f}", None)

    with col2:
        total2 = credit_df.iloc[month_now].sum()
        st.metric("Credit", f"£{total2:,.2f}", None)

    with col3:
        total3 = total1 - total2
        total3_diff = total3 - (debit_df.iloc[month_last].sum() - credit_df.iloc[month_last].sum())
        st.metric("Net worth", f"£{total3:,.2f}", f"£{total3_diff:,.2f}")

view_tab, edit_tab = st.tabs(['View', 'Edit'])
with view_tab:
    st.write("""
    ### These lines represent accounts with actual money in
    You'll notice I've only selected my "main" accounts (missing: Marcus)
    """)
    debit_fig = px.line(
        debit_df,
        labels=dict(
            value='Amount (£)',
            Date=""
        ),
    )
    debit_fig.update_layout(
        legend=dict(
           orientation='h',
           y=-0.3,
           yanchor='auto',
        ),
        legend_title=dict(
            text=None
        )
    )
    st.plotly_chart(fig)
    
    st.write("""
    ### These lines represent credit card debt
    The "primary" account is Barclaycard, the "secondary" account is Natwest
    """)
    credit_fig = px.line(
        credit_df,
        labels=dict(
            value='Amount (£)',
            Date=""
        ),
    )
    credit_fig.update_layout(
        legend=dict(
           orientation='h',
           y=-0.3,
           yanchor='auto',
        ),
        legend_title=dict(
            text=None
        )
    )
    st.line_chart(credit_df)

with edit_tab:
    edited_df = st.data_editor(df)
    edited_df.to_csv('data/newdata.csv')

    if st.button('Update'):
        st.rerun()
