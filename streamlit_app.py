import datetime
import pandas as pd
import plotly.express as px
import streamlit as st
import textwrap

st.set_page_config(layout="centered")  # set to "wide" for widescreen

df = pd.read_csv('data/newdata.csv', index_col='Date')
df.rename({
     'MoneyboxCashISA': 'Cash ISA',
     'MoneyboxS&SISA': 'Stocks/Shares ISA',
     'NatwestSavings': 'Regular Saver',
     'UlsterBank': 'Easy-access Saver',
     'Barclaycard': 'Credit card (primary)',
     'NatwestCredit': 'Credit card (secondary)'
}, axis=1, inplace=True)


# Seperate credit and debit accounts
credit_accs = {'Credit card (primary)', 'Credit card (secondary)'}
credit_cols = list(credit_accs)
debit_accs = set(df.columns).difference(credit_cols)
debit_cols = list(debit_accs)
debit_cols.remove("Marcus")

debit_df = df[debit_cols]
credit_df = df[credit_cols]

# Calculate totals and differences from previous month
month_now = datetime.datetime.now().month - 1
month_last = month_now - 1
debit_now = debit_df.iloc[month_now].sum()
debit_last = debit_df.iloc[month_last].sum()
credit_now = credit_df.iloc[month_now].sum()
credit_last = credit_df.iloc[month_last].sum()
net_now = debit_now - credit_now
net_last = debit_last - credit_last

if net_now - net_last >= 0:
    home_message = "Adam, your finances are looking :green[good]! 💸"
else:
    home_message = "Adam, your finances went :red[down] this month."
    if net_now >= 0:
        home_message += " But overall, you're still :green[positive]! 😀"

multi = f"""
# Adam's Financial Health
**{datetime.datetime.now().strftime('%A %d %B %Y')}**

{home_message}
"""
st.markdown(multi)

if not all(df.iloc[datetime.datetime.now().month-1].notna()):
    st.write(textwrap.dedent("""
        **Warning:** it looks like your data is out of date!
    """))

st.write("### Summary")
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Debit",
            f"£{debit_now:,.2f}",
            f"{debit_now-debit_last:,.2f}"
        )

    with col2:
        st.metric(
            "Credit",
            f"£{credit_now:,.2f}",
            f"{credit_now-credit_last:,.2f}",
            delta_color='inverse'
        )

    with col3:
        st.metric(
            "Net worth",
            f"£{net_now:,.2f}",
            f"{net_now-net_last:,.2f}"
        )

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
    st.plotly_chart(debit_fig)

    st.divider()
    
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
    st.plotly_chart(credit_fig)

with edit_tab:
    edited_df = st.data_editor(df)
    edited_df.to_csv('data/newdata.csv')

    col1, col2 = st.columns(2)
    with col1:
        if st.button('Update'):
            st.rerun()
    
    with col2:
        st.download_button("Download", open(edited_df, 'r'), 'data.csv')
