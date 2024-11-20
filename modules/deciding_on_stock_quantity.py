from xtb_connection import Credit, Minimum_purchase
import asyncio
import yfinance as yf

def stock_partition_in_portfolio(df, login_data):
    """
    Given a data frame containing potential profits and estimation 
    errors, compute the number of each stock to buy. Returns filled
    data frame and number representing unused credit
    """

    # Needed conversion rate from USD to PLN

    # Minimum purchase omount for each stock
    df['minimum_purchase'] = asyncio.run(Minimum_purchase(login_data, df['symbol'] + '.US_9'))

    # Each stock receive equal part of credit
    total_credit = asyncio.run(Credit(login_data))
    singular_credit = total_credit / len(df)
    df['quantity'] = singular_credit // df['minimum_purchase']
    df['used_credit'] = df['quantity'] * df['minimum_purchase']


    # Handling unused credit may be developed
    unused_credit = total_credit - df['used_credit'].sum()
    return df, unused_credit


