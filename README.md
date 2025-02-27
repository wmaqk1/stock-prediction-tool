# Stock Portfolio Management and Prediction Tool

This repository contains a Python-based system designed for managing stock portfolios and predicting future stock prices using data analysis and machine learning techniques. The tool integrates real-time trading capabilities and data processing to provide insights and support automated decision-making.

---

## Features

### 1. Portfolio Management
- **Stock Partition in Portfolio & Stock Choice**:  
 Selects the most promising stocks based on predicted prices and calculates the optimal number to purchase, considering potential profits, estimation errors, available credit and real-time currency exchange rates.
- **Credit Management**:  
  Retrieves available trading credit and handles unused credit after portfolio allocation.
- **Trading Automation**:  
  Includes functionality to:  
  - Buy and sell stocks.  
  - Query stock holdings.  
  - Clear the entire portfolio if needed.

### 2. Machine Learning-Based Price Prediction
- **Price Forecasting**:  
  Implements machine learning models (XGBoost) to predict stock prices.
- **Data Splitting**:  
  Utilizes k-fold cross-validation tailored for time series data to ensure reliable model performance.

### 3. Technical Indicator Analysis
Enhances the dataset with calculated metrics:
- Daily and weekly returns.
- Rolling mean, standard deviation, and median over multiple periods.
- Relative Strength Index (RSI).
- Moving Average Convergence Divergence (MACD).

### 4. Data Enrichment
Adds additional derived features to improve model insights:
- Daily Open-Close and High-Low differences.
- Lagged stock prices for specified periods.
- Seasonal information (e.g., day of the week, month).

---

## Technologies Used
- **Python Libraries**:
  - `asyncio` for asynchronous API interactions.
  - `pandas` and `numpy` for data manipulation.
  - `scikit-learn` for standardization.
  - `xgboost` for machine learning model implementation.
- **External API Integration**:  
  Connects with XTB trading API for real-time stock trading and market data retrieval.

---
## Configuration of the `.env` File

To securely store authentication credentials, create a `.env` file in the root directory of the project. This file should contain data in the following format:

```plaintext
ACCOUNT_ID=17069237
PASSWORD=D4$*2Tx*FHt!4Y#
HOST=ws.xtb.com
TYPE=demo
SAFE=True
```

### Test Overview

The provided scripts include two main testing functions designed to assess the system's prediction accuracy and decision-making effectiveness:

1. **Performance Test**  
   Evaluates the accuracy of stock selection and portfolio allocation, analyzing predicted profits, actual profits, and prediction correctness.

2. **Prediction Test**  
   Focuses on validating price trend predictions (increases or decreases) for individual stocks, measuring overall accuracy and correctness percentages. 

---
