""" Provides functions to load various data """

import datetime
import pandas as pd
import streamlit as st

CURRENT_ACCOUNTS = ['Cash ISA', 'Stocks/Shares ISA', 'Regular Saver', 'Easy-access Saver', 'Marcus']
CREDIT_ACCOUNTS = ['Barclays Credit', 'Natwest Credit']
CASH_ACCOUNTS = ['Cash ISA', 'Regular Saver', 'Easy-access Saver', 'Marcus']
INVESTMENT_ACCOUNTS = ['Stocks/Shares ISA']

@st.cache_data
def calc_date_indices() -> tuple[str]:
    """ Get values for the current and previous month """
    today = datetime.date.today()
    last_month = today.replace(day=1) - datetime.timedelta(days=1)

    return today.strftime('%Y-%m'), last_month.strftime('%Y-%m')

def load_account_data(exclude: list[str] = None) -> pd.DataFrame:
    """ Load and pre-process accounts data """
    # loads bank balances
    df = pd.read_csv('data/accounts.csv', index_col='Date')

    if exclude:
        exclude = set(exclude)
        try:
            df.drop(list(exclude), axis=1, inplace=True)
        except KeyError:
            raise ValueError("Account name(s) from exclude list not found in: "
                        f"{', '.join(df.columns)}") from None
    else:
        exclude = set()

    df['Accounts Total'] = df[list(set(CURRENT_ACCOUNTS).difference(exclude))].transpose().sum()
    df['Credit Total'] = df[list(set(CREDIT_ACCOUNTS).difference(exclude))].transpose().sum()
    df['Total Cash'] = df[list(set(CASH_ACCOUNTS).difference(exclude))].transpose().sum()
    df['Net Total'] = df['Accounts Total'] - df['Credit Total']

    return df

@st.cache_data
def load_creditscores() -> pd.DataFrame:
    """ Load a pre-process credit score data """
    df = pd.read_csv('data/creditscores.csv', index_col='Date',
                    parse_dates=True)

    return df
