import sys
import os

# Add parent directory to the path for module imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from modules.stock_choice import ten_most_promising_stocks
from modules.deciding_on_stock_quantity import stock_partition_in_portfolio
from modules.stock_data_import import import_stock_history


def performance_test(login_data, intervals=4, output_file='selection_results.txt'):
    """
    Verify the accuracy of stock filtration and selection of the most profitable 
    ones made by the stock_choice module and deciding_on_stock_quantity.
    """
    # Import data history
    data_original = import_stock_history()
    data = [stock[:-21] for stock in data_original]

    # Approximate trading days
    half_year_length = 120

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Stock Prediction Test Results\n")

        for run in range(intervals):
            
            data_original = [stock[:-(half_year_length * run + 1)] for stock in data_original]
            data = [stock[:-(half_year_length * run + 1)] for stock in data]
            
            predicted_profit = 0
            actual_profit = 0
            correctly_predicted = 0
            incorrectly_predicted = 0

            program_results = []

            try:
                # Receive proposed set of stocks
                result_df = ten_most_promising_stocks(data)
                result_df, unused_credit = stock_partition_in_portfolio(
                    result_df, login_data)

                for _, row in result_df.iterrows():
                    stock_name = row['symbol']
                    actual_price = find_value(data_original, stock_name)

                    program_results.append({
                        'quantity': row['quantity'],
                        'exchange_rate': row['exchange_rate'],
                        'predicted_price': row['predicted_price'],
                        'actual_price': actual_price,
                        'current_price': row['current_price'],
                    })

                # Calculate prediction accuracy and profits
                for res in program_results:
                    actual_diff = res['actual_price'] - res['current_price']
                    predicted_diff = res['predicted_price'] - \
                        res['current_price']

                    if actual_diff < 0:
                        incorrectly_predicted += 1
                    else:
                        correctly_predicted += 1

                    predicted_profit += res['quantity'] * \
                        predicted_diff * res['exchange_rate']
                    actual_profit += res['quantity'] * \
                        actual_diff * res['exchange_rate']

                f.write(
                    f"Run {run + 1}:\n"
                    f"Correct Predictions: {correctly_predicted}\n"
                    f"Incorrect Predictions: {incorrectly_predicted}\n"
                    f"Predicted Profit: {predicted_profit:.2f}\n"
                    f"Actual Profit: {actual_profit:.2f}\n"
                    f"Unused Credit: {unused_credit:.2f}\n"
                    "--------------------------------------\n"
                )
                print(result_df)

            except Exception as e:
                print(f"Error: {e}")


def find_value(data, stock_name):
    """
    Find the latest closing value for the specified stock.
    """
    for stock in data:
        if stock.empty:
            continue
        if stock.iloc[0].get('Symbol') == stock_name:
            return stock['Close'].iloc[-1]
    raise ValueError(f"Stock {stock_name} not found in the data.")


login_data = {
    "accountId": "17069237",
    "password": "D4$*2Tx*FHt!4Y#",
    "host": "ws.xtb.com",
    "type": "demo",
    "safe": "True",
}

performance_test(login_data)
