from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error

def create_folds(X, n_splits):
    """
    Splits data into training and testing sets using time series split.
    """
    tscv = TimeSeriesSplit(n_splits=n_splits)
    folds = []

    for train_index, val_index in tscv.split(X):
        folds.append((train_index, val_index))
    return folds


def Machine_learning_price_prediction(df):
    """
    Makes price predictions using machine learning.
    Returns tuple containing the predicted price, current price and average squared difference
    """
    # Scaler initialisation
    scaler = StandardScaler()

    # Select features
    X = df[['Volume', 'weekly_return', 'day_of_week', 'month', 'lag_21', 'lag_5', 'Close',
        'rolling_mean_21_days', 'rolling_std_21_days', 'rolling_median_21_days', 'rsi', 'Signal_Line']]

    # Standardize features  
    X_standardized_original = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    # Values for testing
    X_standardized = X_standardized_original[:-21]

     # Select target variable
    y = df[['test']][:-21].values.ravel()

    # Create model
    model = XGBRegressor(
        n_estimators=500, 
        learning_rate=0.05, 
        max_depth=6, 
        subsample=0.8, 
        colsample_bytree=0.8
    )

    # Split data into training and testing sets
    data_sets = create_folds(X_standardized, n_splits=10)
    diff = []
    
    for train_index, val_index in data_sets:
        X_train, X_val = X_standardized.iloc[train_index], X_standardized.iloc[val_index]
        y_train, y_val = y[train_index], y[val_index]

        # Train model
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_val)

        # Calculate metrics
        diff.append(mean_squared_error(y_val, y_pred))
    
    final_pred = model.predict(X_standardized_original.iloc[-1:].values)
    
    current_price = X['Close'].iloc[-1]
    average_diff = np.mean(diff)
    
    return final_pred[0], current_price, average_diff
