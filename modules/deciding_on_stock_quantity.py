from modules.xtb_connection import Credit, Minimum_purchase
import asyncio
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
        exchange_rate = asyncio.run(Minimum_purchase(login_data, 'USDPLN'))
        df['exchange_rate'] = exchange_rate + spread

        # Minimum purchase omount for each stock
        def get_minimum_purchase(row, login_data):
            price_usd = asyncio.run(Minimum_purchase(login_data, row['symbol'] + '.US_9'))
            return price_usd * row['exchange_rate']

        df['minimum_purchase'] = df.apply(lambda row: get_minimum_purchase(row, login_data), axis=1)

        # Each stock receive equal part of credit
        total_credit = asyncio.run(Credit(login_data))
        singular_credit = total_credit / len(df)
        df['quantity'] = (singular_credit / df['minimum_purchase']).apply(math.floor)
        df['used_credit'] = df['quantity'] * df['minimum_purchase']

        # Handling unused credit may be developed
        unused_credit = total_credit - df['used_credit'].sum()
        return df, unused_credit
    

    except Exception as e:
        print(e)
        return None

