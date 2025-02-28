import asyncio
import os
from dotenv import load_dotenv
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
    load_dotenv("login_data.env")
    login_data = {
        "accountId": os.getenv("ACCOUNT_ID"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST"),
        "type": os.getenv("TYPE"),
        "safe": os.getenv("SAFE") == "True"
    }
    
    # Import historical stock data
    stock_history = import_stock_history()

    # Select the ten most promising stocks
    picked_stocks = ten_most_promising_stocks(stock_history)
    print(picked_stocks)
    # Allocate credit among selected stocks
    df, unused_credit = stock_partition(picked_stocks, login_data)

    # Clear the current portfolio
    Clear_Portfolio(login_data)
    df = df.dropna()

    # Purchase stocks
    for _, row in df.iterrows():
        stock_name = row['symbol'] + row['sufix']  # Combine stock symbol and suffix
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

