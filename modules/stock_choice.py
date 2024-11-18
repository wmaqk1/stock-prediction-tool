from stock_forecasting import Machine_learning_price_prediction as predict_prices
from returns_data import data_analysis
from stock_data_import import import_stock_history as import_stock
import pandas as pd
import yfinance

def ten_most_promising_stocks(data):

    df = pd.DataFrame({
        'symbol': [],
        'predicted_price': [],
        'current_price' :[],
        'price_diff': [],
        'actual_diff': [],
        'avarage_diff': []
    })
    for stock in data:
        try:
            stock_with_added_features = data_analysis(stock)
            predicted_price, current_price, actual_price, diff= predict_prices(stock_with_added_features)
            df.loc[len(df)] = [stock['Symbol'][0], predicted_price, current_price, predicted_price - current_price, actual_price - current_price, diff]
        except Exception as e:
            print(f"Error during processing stock {stock['Symbol'][0]}: {e}")
            continue
        
    df = df[df["price_diff"] > 0]
    print(df)
    