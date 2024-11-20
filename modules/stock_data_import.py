import yfinance
import pandas

# Defined function to create table of all S&P 500 component stocks
def import_table():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    stocks = pandas.read_html(url)
    return stocks[0]

# Defined function to create table of historical stock data
def import_stock_history():
    stock_list = import_table()
    data = []
    for index, stock in stock_list[:150].iterrows():
        result = yfinance.download(stock['Symbol'], period='10y')
        result['Symbol'] = stock['Symbol']
        data.append(result)
    return data
