from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
from xgboost import XGBRegressor

def kfold_series(data, n_splits, prediction_window):
    """
    Splits data into training and testing sets using k-fold cross-validation.
    Returns list of tuples containing the start and end indices of each fold.
    """
    try:
        n_samples = len(data)
        if n_samples - n_splits * prediction_window < 50 * n_splits:
            raise ValueError("Not enough data for processing")
        one_period = (n_samples - n_splits * prediction_window) // n_splits

        folds = []
        for i in range(n_splits):
            start = i * one_period
            end = start + one_period
            
            folds.append((end, end + prediction_window))       
        return folds
    except Exception as e:
        return e


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
    model = XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=6, subsample=0.8, colsample_bytree=0.8)

    # Split data into training and testing sets
    data_sets = kfold_series(X_standardized, n_splits=10, prediction_window=1)
    diff = []
    
    for train_index, val_index in data_sets:
        X_train, X_val = X_standardized.iloc[:train_index], X_standardized.iloc[train_index:val_index]
        y_train, y_val = y[:train_index], y[train_index:val_index]

        # Train model
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_val)

        # Calculate metrics
        diff.append(abs(y_val - y_pred) ** 2)
    
    final_pred = model.predict(X_standardized_original.iloc[-1].values.reshape(1, -1))
    correction_factor = 1.05
    
    return final_pred[-1]*correction_factor, X['Close'].iloc[-1], np.average(diff)
