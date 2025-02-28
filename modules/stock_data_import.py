import yfinance as yf
import pandas

def import_table():
    """
    Fetches the table of all S&P 500 component stocks from Wikipedia.
    """
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    stocks = pandas.read_html(url)
    return stocks[0]

def import_stock_history():
    """
    Downloads historical stock data for all S&P 500 component stocks
    for the past 10 years using the yfinance library.
    """
    stock_list = import_table()
    historical_data = []

    for i, stock in stock_list.iterrows():
        symbol = stock['Symbol']
        try:
            data = yf.download(symbol, period='10y')
            data = modify_data_format(data)
            data['Symbol'] = symbol
            historical_data.append(data)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    
    return historical_data

def modify_data_format(data):
    df_old_format = data.copy()
    df_old_format = df_old_format.drop(df_old_format.index[1])

    if isinstance(df_old_format.columns, pandas.MultiIndex):
        symbol = df_old_format.columns.get_level_values(1)[0]
        df_old_format.columns = df_old_format.columns.get_level_values(1)
    else:
        symbol = "UNKNOWN"

    df_old_format.attrs['symbol'] = symbol
    df_old_format.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    return df_old_format
