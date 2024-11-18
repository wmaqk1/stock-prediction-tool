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
        predicted_price, current_price, actual_price, diff= predict_prices(data_analysis(stock))
        df.loc[len(df)] = [stock['Symbol'][0], predicted_price, current_price, predicted_price - current_price, actual_price - current_price, diff]
    
    df = (df.where(df["price_diff"] > 0))
    print(df)
    

def import_table():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    stocks = pd.read_html(url)
    return stocks[0]

# Defined function to create table of historical stock data
def import_stock_history():
    stock_list = import_table()
    data = []
    for index, stock in stock_list[30:50].iterrows():
        result = yfinance.download(stock['Symbol'], period='10y')
        result['Symbol'] = stock['Symbol']
        data.append(result)
    return data

ten_most_promising_stocks(import_stock_history())