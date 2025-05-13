import json
import os
import pandas as pd
import yfinance as yf
from utils import calculate_daily_returns, calculate_portfolio_return, calculate_portfolio_volatility, calculate_sharpe_ratio
import numpy as np

# Load the latest portfolio result
def load_latest_portfolio():
    files = [f for f in os.listdir('.') if f.startswith('portfolio_results_') and f.endswith('.json')]
    if not files:
        raise FileNotFoundError("No portfolio result files found.")
    latest_file = max(files)
    with open(latest_file, 'r') as f:
        return json.load(f)

# Fetch Q1 2025 data without saving to disk
def fetch_q1_2025_data(portfolio):
    data_file = "data2025.csv"
    if os.path.exists(data_file):
        print(f"Loading Q1 2025 data from {data_file}...")
        df = pd.read_csv(data_file)
        return df.pivot(index='Date', columns='Ticker', values='Close')
    else:
        print("Downloading Q1 2025 data...")
        tickers = portfolio['stocks']
        data = yf.download(
            tickers=tickers,
            start="2025-01-01",
            end="2025-03-31",
            interval="1d",
            group_by='ticker',
            auto_adjust=False,
            threads=True
        )
        frames = []
        for ticker in tickers:
            if ticker in data.columns.get_level_values(0):
                df = data[ticker].copy()
                df.reset_index(inplace=True)
                df['Ticker'] = ticker
                frames.append(df)
        merged_df = pd.concat(frames, ignore_index=True)
        merged_df.to_csv(data_file, index=False)
        print(f"Q1 2025 data saved to {data_file}")
        return merged_df.pivot(index='Date', columns='Ticker', values='Close')

# Main testing logic
if __name__ == "__main__":
    portfolio = load_latest_portfolio()
    q1_data = fetch_q1_2025_data(portfolio)
    daily_returns = calculate_daily_returns(q1_data)
    weights = np.array([portfolio['weights'][stock] for stock in portfolio['stocks']])
    metrics = {
        'sharpe_ratio': calculate_sharpe_ratio(daily_returns.values, weights),
        'annual_return': calculate_portfolio_return(daily_returns.values, weights),
        'annual_volatility': calculate_portfolio_volatility(daily_returns.values, weights)
    }
    print("Q1 2025 Portfolio Metrics:")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.4f}")
    print(f"Annual Return: {metrics['annual_return']:.4f}")
    print(f"Annual Volatility: {metrics['annual_volatility']:.4f}")
