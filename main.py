from modules.deciding_on_stock_quantity import stock_partition_in_portfolio as stock_partition
from modules.stock_choice import ten_most_promising_stocks 
from modules.stock_data_import import import_stock_history

def main():

    login_data = {
    "accountId": "17069237",
    "password": "D4$*2Tx*FHt!4Y#",
    "host": "ws.xtb.com",
    "type": "demo",
    "safe": "True",
    }

    stock_history = import_stock_history()
    picked_stocks = ten_most_promising_stocks(stock_history)
    df, unused_credit = stock_partition(picked_stocks, login_data)
    print(df)
    potential_result = 0
    actual_result = 0
    for index, row in df.iterrows():
        potential_result += row['price_diff'] * row['quantity'] * row['exchange_rate']
        actual_result += row['actual_diff'] * row['quantity'] * row['exchange_rate']
        print(potential_result, actual_result, unused_credit)
    
main()

