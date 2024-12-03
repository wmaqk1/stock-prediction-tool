from modules.stock_forecasting import Machine_learning_price_prediction as predict_prices
from modules.returns_data import data_analysis
from modules.stock_data_import import import_stock_history as import_stock
import pandas as pd

def ten_most_promising_stocks(data):
    """
    Uses implemented ML model for predicting stock prices and based 
    on their values and uncertainty chooses 10 most promising stocks 
    in terms of profit.
    """
    df = pd.DataFrame({
        'symbol': [],
        'predicted_price': [],
        'current_price' :[],
        'price_diff': [],
        'actual_diff': [],
        'avarage_diff_squared': []
    })
    for stock in data:
        try:
            # Analyze the stock data
            stock_with_added_features = data_analysis(stock)
            # Predict prices
            predicted_price, current_price, diff = predict_prices(stock_with_added_features)
            
            # Ensure the stock has a valid symbol
            symbol = stock.get('Symbol', [None])[0]
            if symbol:
                # Add results to the DataFrame
                df.loc[len(df)] = [
                    symbol,
                    predicted_price,
                    current_price,
                    predicted_price - current_price,
                    diff
                ]
            else:
                print("Error: No valid symbol found for the stock.")
        except Exception as e:
            print(f"Error processing stock: {str(e)}")
 
    try:
        # Filter rows where the 'price_diff' column is greater than 0 and squared_diff < 2 
        df = df[df['price_diff'] > 0]
        df = df[df['avarage_diff_squared'] < 2]
        df['profit_to_value'] = df['price_diff'] / df['current_price']
        # Retain only the top 10 rows based on the sorted DataFrame
        df = df.sort_values(by='profit_to_value', ascending=False)
        df = df[:10]
        return df
    except Exception as e:
        print(f"Lack of promising stocks: {e}")
        return None

