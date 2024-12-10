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

    for _, stock in stock_list.iterrows():
        symbol = stock['Symbol']
        try:
            data = yf.download(symbol, period='10y')
            data['Symbol'] = symbol
            historical_data.append(data)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    
    return historical_data
