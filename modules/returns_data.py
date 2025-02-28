def add_returns(data_frame, period, label):
    """Add return column for a specified time period."""
    data_frame[f'{label}_return'] = (
        data_frame['Close'] - data_frame['Close'].shift(period)
    )
    return data_frame


def add_rolling_statistic(data_frame, type_name):
    """Add rolling statistics (mean, std, median) for specified periods."""
    periods = [7, 21, 60, 100]
    for period in periods:
        data_frame[f'rolling_mean_{period}_days'] = data_frame[type_name].rolling(window=period).mean()
        data_frame[f'rolling_std_{period}_days'] = data_frame[type_name].rolling(window=period).std()
        data_frame[f'rolling_median_{period}_days'] = data_frame[type_name].rolling(window=period).median()
    return data_frame


def daily_open_close_diff(data_frame):
    """Add daily difference between Open and Close prices."""
    data_frame['Close-Open diff'] = data_frame['Close'] - data_frame['Open']
    return data_frame


def daily_high_low_diff(data_frame):
    """Compute daily difference between lowest and highest price."""
    data_frame['High-Low diff'] = data_frame['High'] - data_frame['Low']
    return data_frame


def rsi_implementation(data_frame, window):
    """Compute the Relative Strength Index (RSI)."""
    diff = data_frame['Close'].diff()
    gain = diff.where(diff > 0, 0).rolling(window=window).mean()
    loss = -diff.where(diff < 0, 0).rolling(window=window).mean()
    data_frame['rsi'] = 100 - (100 / (1 + gain / loss))
    return data_frame


def create_lagged_features(df, lags=[1, 5, 21]):
    """Add lagged features for stock prices."""
    for lag in lags:
        df[f'lag_{lag}'] = df['Close'].shift(lag)
    return df


def macd_implementation(data_frame):
    """Compute and add MACD and Signal Line for stock prices."""
    data_frame['EMA_12'] = data_frame['Close'].ewm(span=12, adjust=False).mean()
    data_frame['EMA_26'] = data_frame['Close'].ewm(span=26, adjust=False).mean()
    data_frame['MACD'] = data_frame['EMA_12'] - data_frame['EMA_26']
    data_frame['Signal_Line'] = data_frame['MACD'].ewm(span=9, adjust=False).mean()
    return data_frame


def data_analysis(df):
    """Add additional technical indicators to the data frame."""
    try:
        # Add returns for daily, weekly, and monthly periods
        periods = {
            'daily': 1,
            'weekly': 5,
            'monthly': 21,
        }
        for label, period in periods.items():
            df = add_returns(df, period, label)

        # Add rolling statistics
        df = add_rolling_statistic(df, 'Close')

        # Add daily differences
        df = daily_open_close_diff(df)
        df = daily_high_low_diff(df)

        # Add RSI and MACD
        df = rsi_implementation(df, 14)
        df = macd_implementation(df)

        # Add day of the week and month features
        df['day_of_week'] = df.index.dayofweek
        df['month'] = df.index.month

        # Add lagged features
        df = create_lagged_features(df)

        # Remove rows with missing data and add a shifted test column
        df = df.dropna().copy()
        df['test'] = df['Close'].shift(-21)

        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

