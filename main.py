import asyncio
from modules.stock_forecasting import Machine_learning_price_prediction
from modules.returns_data import data_analysis
from modules.deciding_on_stock_quantity import stock_partition_in_portfolio as stock_partition
from modules.stock_choice import ten_most_promising_stocks
from modules.stock_data_import import import_stock_history
from modules.xtb_connection import Buy_Stock, Clear_Portfolio


def main():
    """
    Main function to execute the stock trading process
    """

    # Login data for the XTB API
    login_data = {
        "accountId": "17069237",
        "password": "D4$*2Tx*FHt!4Y#",
        "host": "ws.xtb.com",
        "type": "demo",
        "safe": "True",
    }

    # Import historical stock data
    stock_history = import_stock_history()

    # Select the ten most promising stocks
    picked_stocks = ten_most_promising_stocks(stock_history)

    # Allocate credit among selected stocks
    df, unused_credit = stock_partition(picked_stocks, login_data)

    # Clear the current portfolio
    Clear_Portfolio(login_data)

    # Purchase stocks
    for _, row in df.iterrows():
        stock_name = row['symbol'] + row[-3]  # Combine stock symbol and suffix
        quantity = row[-2]  # Extract quantity to buy
        result = asyncio.run(Buy_Stock(login_data, stock_name, quantity))
        if not result:
            print(f"Stock: {stock_name} purchase was not successful")

    # Calculate potential profit
    potential_result = sum(
        row['price_diff'] * row['quantity'] * row['exchange_rate']
        for _, row in df.iterrows()
    )

    # Print potential result and unused credit
    print(f"Potential result: {potential_result}")
    print(f"Unused credit: {unused_credit}")

    # Print final DataFrame
    print(df)


if __name__ == "__main__":
    main()

