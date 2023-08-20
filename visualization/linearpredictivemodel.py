# -*- coding: utf-8 -*-
"""linearPredictiveModel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-aXksmcZZC99uLALc5U6KBQe4-IoTNgu
"""

!pip install fbprophet

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Define the top 10 virtual coins
top_coins = ['BTC', 'ETH', 'ADA', 'BNB', 'XRP', 'SOL', 'DOT', 'DOGE', 'USDT', 'AVAX']

def fetch_coin_data(coin_symbol, start_date, end_date):
    coin_data = yf.download(f'{coin_symbol}-USD', start=start_date, end=end_date)
    coin_monthly = coin_data['Adj Close'].resample('M').last().reset_index()
    coin_monthly['Month'] = coin_monthly['Date'].dt.month
    coin_monthly['Year'] = coin_monthly['Date'].dt.year
    return coin_monthly

def linear_regression_forecast(coin_monthly, horizon):
    X = coin_monthly[['Month', 'Year']]
    y = coin_monthly['Adj Close']
    model = LinearRegression()
    model.fit(X, y)

    next_month = coin_monthly['Month'].iloc[-1] + horizon
    next_year = coin_monthly['Year'].iloc[-1]
    if next_month > 12:
        next_month -= 12
        next_year += 1

    next_price = model.predict([[next_month, next_year]])
    return next_price[0]

def main():
    start_date = '2021-01-01'
    end_date = '2023-08-20'
    horizon_range = range(1, 13)

    # Create a 5x5 array of subplots
    fig, axes = plt.subplots(nrows=5, ncols=2, figsize=(15, 30))
    axes = axes.ravel()

    for i, coin_symbol in enumerate(top_coins):
        ax = axes[i]

        coin_monthly = fetch_coin_data(coin_symbol, start_date, end_date)
        forecast_prices = []

        for horizon in horizon_range:
            forecast_price = linear_regression_forecast(coin_monthly, horizon)
            forecast_prices.append(forecast_price)

        forecast_dates = [coin_monthly['Date'].iloc[-1] + pd.DateOffset(months=horizon) for horizon in horizon_range]
        ax.plot(coin_monthly['Date'], coin_monthly['Adj Close'], label='Historical', color='black')
        ax.plot(forecast_dates, forecast_prices, label='Forecast', linestyle='dashed')
        ax.set_title(coin_symbol)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend()
        ax.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()

