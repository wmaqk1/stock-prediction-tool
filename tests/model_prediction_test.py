import sys
import os
import numpy as np

# Add parent directory to the path for module imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from modules.returns_data import data_analysis
from modules.stock_forecasting import Machine_learning_price_prediction
from modules.stock_data_import import import_stock_history

def prediction_test(intervals=4, output_file='prediction_results.txt'):
    """
    Verify the accuracy of price increase and decrease predictions made 
    by the stock_forecasting module for individual stocks.
    
    Args:
        intervals (int): Number of intervals to evaluate predictions over.
        output_file (str): File name for storing prediction results.
    """
    # Import stock data history
    data = import_stock_history()

    # Approximate trading days in half a year
    half_year_length = 120

    # Initialize accuracy lists
    overall_accuracy_list = []
    increase_accuracy_list = []

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Stock Prediction Test Results\n")

        for run in range(intervals):
            result_array = []

            for stock in data:
                try:
                    stock = data_analysis(stock)
                    stock = stock.dropna()

                    # Use stock data excluding the current interval
                    stock = stock[:-(half_year_length * run + 1)]

                    if not stock['test'].empty:
                        actual_price = stock['test'].iloc[-1]
                        forecast, current_price, diff = Machine_learning_price_prediction(stock)

                        # Collect results: actual, forecasted price, and differences
                        result_array.append((actual_price, forecast, current_price, diff))
                except Exception as e:
                    print(f"Error: {e}")

            # Initialize prediction counters
            correctly_predicted_increase = 0
            correctly_predicted_decrease = 0
            incorrectly_predicted_increase = 0
            incorrectly_predicted_decrease = 0

            for actual_price, forecast, current_price, diff in result_array:
                actual_diff = actual_price - current_price
                predicted_diff = forecast - current_price

                # Classify prediction outcomes
                if predicted_diff < 0 and actual_diff > 0:
                    incorrectly_predicted_decrease += 1
                elif predicted_diff > 0 and actual_diff < 0:
                    incorrectly_predicted_increase += 1
                elif predicted_diff < 0 and actual_diff < 0:
                    correctly_predicted_decrease += 1
                elif predicted_diff > 0 and actual_diff > 0:
                    correctly_predicted_increase += 1

            # Log results for the current interval
            run_results = (
                f"\nNumber of incorrectly predicted increases: {incorrectly_predicted_increase}\n"
                f"Number of incorrectly predicted decreases: {incorrectly_predicted_decrease}\n"
                f"Number of correctly predicted decreases: {correctly_predicted_decrease}\n"
                f"Number of correctly predicted increases: {correctly_predicted_increase}\n"
            )
            print(run_results)
            f.write(run_results)

            # Calculate accuracy metrics
            total_predictions = len(result_array)
            accuracy_percentage = (
                (correctly_predicted_increase + correctly_predicted_decrease) / total_predictions
            ) * 100
            overall_accuracy_list.append(accuracy_percentage)

            increase_accuracy = (
                correctly_predicted_increase /
                (correctly_predicted_increase + incorrectly_predicted_increase)
            ) * 100
            increase_accuracy_list.append(increase_accuracy)

            # Log accuracy results
            accuracy_results = (
                f"\nOverall correctness percentage: {accuracy_percentage:.2f}%\n"
                f"Increase prediction correctness: {increase_accuracy:.2f}%\n"
            )
            print(accuracy_results)
            f.write(accuracy_results)

        # Calculate and log average accuracies
        avg_overall_accuracy = np.average(overall_accuracy_list)
        avg_increase_accuracy = np.average(increase_accuracy_list)

        summary_results = (
            f"\nAverage trend prediction accuracy: {avg_overall_accuracy:.2f}%\n"
            f"Average increase prediction accuracy: {avg_increase_accuracy:.2f}%\n"
        )
        print(summary_results)
        f.write(summary_results)


if __name__ == "__main__":
    prediction_test()

