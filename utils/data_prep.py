""" Provides functions to load various data """

import pandas as pd
import streamlit as st

CURRENT_ACCOUNTS = ['MoneyboxCashISA', 'MoneyboxS&SISA', 'NatwestSavings', 'UlsterBank']
CURRENT_ACCOUNTS_DESC = ['Cash ISA', 'Stocks/Shares ISA', 'Regular Saver', 'Easy-access Saver']
CREDIT_ACCOUNTS = ['Barclaycard', 'NatwestCredit']
CREDIT_ACCOUNTS_DESC = ['Barclays Credit', 'Natwest Credit']

@st.cache_data
def load_account_data(exclude: list[str] = None) -> pd.DataFrame:
    """ Load and pre-process accounts data """
    # loads bank balances
    df = pd.read_csv('data/newdata.csv', index_col='Date')
    df.rename(dict(zip(CURRENT_ACCOUNTS + CREDIT_ACCOUNTS,
                       CURRENT_ACCOUNTS_DESC + CREDIT_ACCOUNTS_DESC)),
              axis=1, inplace=True)

    try:
        if exclude:
            df.drop(exclude, axis=1, inplace=True)
    except KeyError:
        raise ValueError("Account name(s) from exclude list not found in: "
                        f"{', '.join(df.columns)}") from None

    # Add totals
    df['AccTotals'] = df[CURRENT_ACCOUNTS_DESC].transpose().sum()
    df['CredTotals'] = df[CREDIT_ACCOUNTS_DESC].transpose().sum()
    df['NetTotals'] = df['AccTotals'] - df['CredTotals']

    return df

@st.cache_data
def load_creditscores() -> pd.DataFrame:
    """ Load a pre-process credit score data """
    df = pd.read_csv('data/creditscores.csv', index_col='Date',
                    parse_dates=True)

    return df
