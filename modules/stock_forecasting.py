from returns_data import data_analysis
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd
import yfinance
from xgboost import XGBRegressor

df = yfinance.download('BA', period='10y')
df, days_for_prediction = data_analysis(df)

# Split data into training and testing sets
def kfold_series(data, n_splits, prediction_window):
    n_samples = len(data)
    if n_samples - n_splits * prediction_window < 100 * n_splits:
        raise ValueError("Not enough data for processing")
    one_period = (n_samples - n_splits * prediction_window) // n_splits
    folds = []

    for i in range(n_splits):
        start = i * one_period
        end = start + one_period
        
        folds.append((end, end + prediction_window))
    
    return folds


def Machine_learning_price_prediction(df, days_for_prediction):
    # Scaler initialisation
    scaler = StandardScaler()


    # Parameters chosen for testing
    X = df[['Open', 'High', 'Low', 'Close', 'Volume',
        'weekly_return', 'monthly_return', 'day_of_week', 'month', 'lag_21',
        'rolling_mean_21_days', 'rolling_std_21_days', 'rolling_median_21_days',
        'rolling_mean_60_days', 'rolling_std_60_days', 'rolling_median_60_days',
        'rolling_mean_100_days', 'rolling_std_100_days', 'rolling_median_100_days',
            'Close-Open diff', 'High-Low diff', 'rsi', 'Signal_Line', 'lag_21_rsi']]
        
    X_standardized = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    X_learn = X_standardized[:-21]

    # Information about next weeks value
    y = df[['test']].dropna()
    y = y.values.ravel()

    # Creating model used for prices predictions
    model = XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=6, subsample=0.8, colsample_bytree=0.8)

    data_sets = kfold_series(X_learn, n_splits=15, prediction_window=21)
    r2 = []
    
    for train_index, val_index in data_sets:
        X_train, X_val = X_learn.iloc[:train_index], X_learn.iloc[train_index:val_index]
        y_train, y_val = y[:train_index], y[train_index:val_index]

        # Train the model
        model.fit(X_train, y_train)

        # Predict on validation set
        y_pred = model.predict(X_val)

        # Calculate metrics
        r2.append(r2_score(y_val, y_pred))
    
    prediction = model.predict(X_standardized)
    
    return prediction, np.average(r2)
prediction, r2 = Machine_learning_price_prediction(df, days_for_prediction)
print(r2)
# Output the results
import matplotlib.pyplot as plt

#plt.plot(y_val, label="Rzeczywiste")
plt.plot(prediction, label="Prognozowane")
plt.legend()
plt.title("Porównanie rzeczywistych i prognozowanych cen")
plt.show()