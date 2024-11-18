# Adds a return column for a specified time period.
def add_returns(data_frame, period, label):
    data_frame[f'{label}_return'] = data_frame['Adj Close'] - data_frame['Adj Close'].shift(period)
    return data_frame

# Adds statistics information for certain periods of time
def add_rolling_statistic(data_frame, type_name):
    periods = [7, 21, 60, 100]
    for period in periods:
        data_frame[f'rolling_mean_{period}_days'] = data_frame[f'{type_name}'].rolling(window=period).mean()
        data_frame[f'rolling_std_{period}_days'] = data_frame[f'{type_name}'].rolling(window=period).std()
        data_frame[f'rolling_median_{period}_days'] = data_frame[f'{type_name}'].rolling(window=period).median()
    return data_frame

def daily_open_close_diff(data_frame):
    data_frame['Close-Open diff'] = data_frame['Close'] - data_frame['Open']
    return data_frame

# Compute daily difference between lowest and highest price
def daily_high_low_diff(data_frame):
    data_frame['High-Low diff'] = data_frame['High'] - data_frame['Low']
    return data_frame

# Compute the Relative Strength Index (RSI)
def rsi_implementation(data_frame, window):
    diff = data_frame['Close'].diff()
    gain = (diff.where(diff > 0, 0)).rolling(window=window).mean()
    loss = (-diff.where(diff < 0, 0)).rolling(window=window).mean()
    data_frame['rsi'] = 100 - (100 / (1 + gain/loss))
    return data_frame

# Standard MACD calculation
def macd_implementation(data_frame):
    data_frame['EMA_12'] = data_frame['Close'].ewm(span=12, adjust=False).mean()
    data_frame['EMA_26'] = data_frame['Close'].ewm(span=26, adjust=False).mean()
    data_frame['MACD'] = data_frame['EMA_12'] - data_frame['EMA_26']
    data_frame['Signal_Line'] = data_frame['MACD'].ewm(span=9, adjust=False).mean()
    return data_frame

def data_analysis(df):
    periods = {
    'daily': 1,
    'weekly': 5,
    'monthly': 21,
    }
    for label, period in periods.items():
        df = add_returns(df, period, label)

    df = add_rolling_statistic(df, 'Adj Close')

    df = daily_open_close_diff(df)

    df = daily_high_low_diff(df)

    df = rsi_implementation(df, 14)

    df = macd_implementation(df)

    df['day_of_week'] = df.index.dayofweek

    df['month'] = df.index.month

    df['lag_21'] = df['Close'].shift(21)

    df['lag_21_rsi'] = df['rsi'].shift(21)

    df = df.dropna()
    # Currently there is no acces to future predictions due to dropna usage
    df['test'] = df['Close'].shift(-21)
    days_for_prediction = 21
    return df, days_for_prediction