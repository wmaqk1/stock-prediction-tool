import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from modules.returns_data import data_analysis
from modules.stock_forecasting import Machine_learning_price_prediction
from modules.stock_data_import import import_stock_history
import numpy as np


def prediction_test(intervals=4, output_file='prediction_results.txt'):
    '''
    Verify the accuracy of price increase and decrease predictions made 
    by the stock_forecasting module for singular stocks.
    '''
    # Import data history
    data = import_stock_history()
    
    # Aproximate trading days
    half_year_length = 120
    
    overall_accuracy_list = []
    increase_accuracy_list = []
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Stock Prediction Test Results\n")
    
        for run in range(intervals):
        
            result_array = []

            for stock in data:
                try:
                    stock = data_analysis(stock)
                    stock = stock.dropna()
                    stock = stock[:-(half_year_length * run + 1)]
                    if not stock['test'].empty:
                        actual_price = stock['test'].iloc[-1]

                        forecast, current_price, diff = Machine_learning_price_prediction(
                            stock)
                        # Adds actual and predicted price as well as current price and squared difference
                        result_array.append((actual_price, forecast, current_price, diff))
                except Exception as e:
                    print(f"Eror: {e}")

            # Sets counters
            correctly_predicted_increase = 0
            correctly_predicted_decrease = 0
            incorrectly_predicted_decrease = 0
            incorrectly_predicted_increase = 0

            for actual_price, forecast, current_price, diff in result_array:

                actual_diff = actual_price - current_price
                predicted_diff = forecast - current_price
                
                if predicted_diff < 0 and actual_diff > 0:
                    incorrectly_predicted_decrease += 1
                elif predicted_diff > 0 and actual_diff < 0:
                    incorrectly_predicted_increase += 1
                elif predicted_diff < 0 and actual_diff < 0:
                    correctly_predicted_decrease += 1
                elif predicted_diff > 0 and actual_diff > 0:
                    correctly_predicted_increase += 1

            run_results = (
                f"\nNumber of incorrectly predicted increases: {incorrectly_predicted_increase}\n"
                f"Number of incorrectly predicted decreases: {incorrectly_predicted_decrease}\n"
                f"Number of correctly predicted decreases: {correctly_predicted_decrease}\n"
                f"Number of correctly predicted increases: {correctly_predicted_increase}\n"
            )
            print(run_results)
            f.write(run_results)
            
            accuracy_percentage = ((correctly_predicted_increase + correctly_predicted_decrease) / len(result_array)) * 100
            overall_accuracy_list.append(accuracy_percentage)
            
            
            increase_accuracy = (correctly_predicted_increase / (correctly_predicted_increase + incorrectly_predicted_increase)) * 100
            increase_accuracy_list.append(increase_accuracy)
            
            accuracy_results = (
                f"\nOverall correctness percentage: {accuracy_percentage:.2f}%\n"
                f"Increase prediction correctness: {increase_accuracy:.2f}%\n"
            )
            print(accuracy_results)
            f.write(accuracy_results)
        
        avg_overall_accuracy = np.average(overall_accuracy_list)
        avg_increase_accuracy = np.average(increase_accuracy_list)

        summary_results = (
            f"\nAverage trend prediction accuracy: {avg_overall_accuracy:.2f}%\n"
            f"Average increase prediction accuracy: {avg_increase_accuracy:.2f}%\n"
        )
        print(summary_results)
        f.write(summary_results)
    
prediction_test()
