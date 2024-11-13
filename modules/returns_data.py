import pandas as pd
import yfinance as yf

df = pd.DataFrame({
    'Date': ['01-12-2001', '02-12-2001', '03-12-2001', '04-12-2001', '05-12-2001', '06-12-2001', '07-12-2001'],
    'Price': [4, 1, 2, 3, 4, 4, 1]
})
def add_daily_returns(data_frame, name):
    data_frame[f'daily_return_{name}'] = data_frame[f'{name}'] - data_frame[f'{name}'].shift(1)
    return data_frame

def add_weekly_returns(data_frame, name):
    data_frame[f'weekly_return_{name}'] = data_frame[f'{name}'] - data_frame[f'{name}'].shift(7)
    return data_frame

def add_monthly_returns(data_frame, name):
    data_frame[f'monthly_return_{name}'] = data_frame[f'{name}'] - data_frame[f'{name}'].shift(30)
    return data_frame

def add_yearly_returns(data_frame, name):
    data_frame[f'yearly_return_{name}'] = data_frame[f'{name}'] - data_frame[f'{name}'].shift(365)
    return data_frame

# mean of all past prices not including current one
def mean(data_frame, name):
    data_frame[f'mean_{name}'] = data_frame[f'{name}'].expanding().mean().shift(1)
    return data_frame

def rolling_statistic(data_frame, type_name):
    periods = [3, 7, 10, 30, 100]
    for period in periods:
        data_frame[f'rolling_mean_{period}_days'] = data_frame[f'{type_name}'].rolling(window=period).mean()
        data_frame[f'rolling_std_{period}_days'] = data_frame[f'{type_name}'].rolling(window=period).std()
        data_frame[f'rolling_median_{period}_days'] = data_frame[f'{type_name}'].rolling(window=period).median()
    return data_frame

def data_analysis(data_frame, price_type):
    data_frame = add_daily_returns(data_frame, price_type)
    data_frame = add_weekly_returns(data_frame, price_type)
    data_frame = add_monthly_returns(data_frame, price_type)
    data_frame = add_yearly_returns(data_frame, price_type)
    data_frame = mean(data_frame, price_type)
    data_frame = rolling_statistic(data_frame, price_type)
    print(data_frame[360:])

result = yf.download('AAPL', period='10y')
print(result)
data_analysis(result, 'Open')