from modules.xtb_connection import Credit, Minimum_purchase
import asyncio
import pandas as pd
import math


def stock_partition_in_portfolio(df, login_data):
    """
    Given a data frame containing potential profits and estimation 
    errors, compute the number of each stock to buy. Returns filled
    data frame and number representing unused credit
    """

    try:
        # Needed conversion rate from USD to PLN
        spread = 0.02

        exchange_rate = asyncio.run(
            Minimum_purchase(login_data, 'USDPLN')) + spread
        df['exchange_rate'] = exchange_rate

        # Minimum purchase omount for each stock and sufix information
        def get_minimum_purchase(row, login_data):
            price_usd = asyncio.run(
                Minimum_purchase(login_data, row[0] + '.US_9'))
            sufix = '.US_9'
            if price_usd is None:
                price_usd = asyncio.run(
                    Minimum_purchase(login_data, row[0] + '.US'))
                sufix = '.US'
            if price_usd is None:
                sufix = None
                return None, sufix
            return round(price_usd * exchange_rate, 4), sufix

        df[['minimum_purchase', 'sufix']] = df.apply(
            lambda row: pd.Series(get_minimum_purchase(row, login_data)), axis=1)

        # Each stock receive equal part of credit
        total_credit = asyncio.run(Credit(login_data))
        singular_credit = total_credit / len(df)
        df['quantity'] = (singular_credit /
                          df['minimum_purchase']).apply(math.floor)
        df['used_credit'] = df['quantity'] * df['minimum_purchase']

        # Handling unused credit may be developed
        unused_credit = total_credit - df['used_credit'].sum()
        return df, unused_credit

    except Exception as e:
        print(e)
        return None
