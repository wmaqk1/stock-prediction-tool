import asyncio
import pandas as pd
import math
from modules.xtb_connection import Credit, Minimum_purchase


def stock_partition_in_portfolio(df, login_data):
    """
    Given a DataFrame containing potential profits and estimation 
    errors, compute the number of each stock to buy. Returns the 
    filled DataFrame and a number representing unused credit.
    """

    try:
        # Add a spread to the USD to PLN conversion rate
        spread = 0.02
        exchange_rate = asyncio.run(Minimum_purchase(login_data, 'USDPLN')) + spread
        df['exchange_rate'] = exchange_rate

        # Function to get the minimum purchase amount and suffix for each stock
        def get_minimum_purchase(row, login_data):
            price_usd = asyncio.run(Minimum_purchase(login_data, f"{row[0]}.US_9"))
            sufix = '.US_9'

            if price_usd is None:
                price_usd = asyncio.run(Minimum_purchase(login_data, f"{row[0]}.US"))
                sufix = '.US'

            if price_usd is None:
                sufix = None
                return None, sufix

            return round(price_usd * exchange_rate, 4), sufix

        # Apply the minimum purchase calculation to each row
        df[['minimum_purchase', 'sufix']] = df.apply(
            lambda row: pd.Series(get_minimum_purchase(row, login_data)), axis=1
        )

        # Retrieve total credit and allocate an equal portion to each stock
        total_credit = asyncio.run(Credit(login_data))
        singular_credit = total_credit / len(df)

        df['quantity'] = (singular_credit / df['minimum_purchase']).apply(math.floor)
        df['used_credit'] = df['quantity'] * df['minimum_purchase']

        # Calculate unused credit
        unused_credit = total_credit - df['used_credit'].sum()

        return df, unused_credit

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
