import os
import json
from datetime import datetime
from get_data import get_data
import pandas as pd

def check_and_get_data(data_path: str, start_date: str, end_date: str) -> None:
    """Check if data exists and get it if needed."""
    print(f"Checking if {data_path} exists")
    if not os.path.exists(data_path):
        get_data(start_date, end_date)

def load_price_data(data_path: str) -> pd.DataFrame:
    """Load price data from CSV and pivot it to the right format."""
    print("Loading data...")
    df = pd.read_csv(data_path)
    return df.pivot(index='Date', columns='Ticker', values='Close')

def save_results(portfolio: dict, timestamp: str) -> str:
    """Save portfolio results to a JSON file."""
    results_file = f"portfolio_results_{timestamp}.json"
    with open(results_file, 'w') as f:
        json.dump(portfolio, f, indent=4)
    return results_file

def print_portfolio_summary(portfolio: dict, execution_time: float, results_file: str) -> None:
    """Print a summary of the portfolio results."""
    print(f"\nOptimization completed in {execution_time:.2f} seconds")
    print(f"\nOptimal Portfolio Found!")
    print(f"Sharpe Ratio: {portfolio['sharpe_ratio']:.4f}")
    print(f"Annual Return: {portfolio['annual_return']:.4f}")
    print(f"Annual Volatility: {portfolio['annual_volatility']:.4f}")
    print("\nPortfolio Weights:")
    
    # Sort weights by value in descending order for better presentation
    sorted_weights = sorted(portfolio['weights'].items(), key=lambda x: x[1], reverse=True)
    for stock, weight in sorted_weights:
        print(f"{stock}: {weight:.4f}")
    
    print(f"\nDetailed results saved to {results_file}") 