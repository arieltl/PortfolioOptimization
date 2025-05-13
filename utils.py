import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
from itertools import combinations

def calculate_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily returns for a price dataframe.
    
    Args:
        prices: DataFrame with stock prices
        
    Returns:
        DataFrame with daily returns
    """ 
    return prices.pct_change().dropna()

def calculate_portfolio_metrics_vectorized(returns_array: np.ndarray, weights_batch: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate portfolio metrics for a batch of weight vectors at once.
    
    Args:
        returns_array: NumPy array with daily returns (days x assets)
        weights_batch: NumPy array with multiple weight vectors (portfolios x assets)
        
    Returns:
        Tuple of (sharpe_ratios, annual_returns, annual_volatilities)
    """
    # Calculate daily portfolio returns for all weight combinations (Rp = r * w)
    # We can do this efficiently by first calculating mean returns for each asset
    # and then multiplying by weights, which is mathematically equivalent to
    # calculating daily returns and then taking the mean
    mean_returns = np.mean(returns_array, axis=0) * 252  # Shape: (assets,)
    portfolio_returns = weights_batch @ mean_returns  # Shape: (portfolios,)

    cov_matrix = np.cov(returns_array.T)  # Shape: (assets x assets)
    cov_w = np.dot(weights_batch, cov_matrix.T)  # Shape: (portfolios x assets)
    portfolio_variances = np.sum(cov_w * weights_batch, axis=1)  # Shape: (portfolios,)
    portfolio_volatilities = np.sqrt(portfolio_variances) * np.sqrt(252)  # Annualize
    
    # Calculate Sharpe ratios
    sharpe_ratios = portfolio_returns / portfolio_volatilities
    
    return sharpe_ratios, portfolio_returns, portfolio_volatilities

def calculate_portfolio_return(returns_array: np.ndarray, weights: np.ndarray) -> float:
    """Calculate the annualized portfolio return.
    
    Args:
        returns_array: NumPy array with daily returns
        weights: Array of portfolio weights
        
    Returns:
        Annualized portfolio return
    """
    # Faster matrix operation
    mean_returns = np.mean(returns_array, axis=0) * 252
    return float(np.sum(mean_returns * weights))

def calculate_portfolio_volatility(returns_array: np.ndarray, weights: np.ndarray) -> float:
    """Calculate the annualized portfolio volatility.
    
    Args:
        returns_array: NumPy array with daily returns
        weights: Array of portfolio weights
        
    Returns:
        Annualized portfolio volatility
    """
    # Calculate covariance matrix directly using numpy
    cov_matrix = np.cov(returns_array.T) * 252
    
    # Faster matrix operation using numpy directly
    portfolio_variance = weights @ cov_matrix @ weights
    return float(np.sqrt(portfolio_variance))

def calculate_sharpe_ratio(returns_array: np.ndarray, weights: np.ndarray) -> float:
    """Calculate the Sharpe Ratio for a portfolio.
    
    Args:
        returns_array: NumPy array with daily returns
        weights: Array of portfolio weights
        
    Returns:
        Sharpe Ratio
    """
    portfolio_return = calculate_portfolio_return(returns_array, weights)
    portfolio_volatility = calculate_portfolio_volatility(returns_array, weights)
    return float(portfolio_return / portfolio_volatility)

def generate_valid_weights(n_assets: int, n_simulations: int = 1000) -> np.ndarray:
    """Generate valid random portfolio weights using vectorized operations.
    
    Returns:
        Array of valid weight vectors (each row is a valid weight vector)
    """
    # First, generate significantly more weights to account for filtering
    multiplier = 3  # Generate 3x more than needed to ensure we get enough
    target_weights = min(n_simulations * multiplier, 10000)
    
    weights = np.random.random((target_weights, n_assets))
    weights = weights / weights.sum(axis=1, keepdims=True)
    valid_mask = np.all(weights <= 0.2, axis=1)
    valid_weights = weights[valid_mask]
    
    # If we don't have enough weights, generate more
    if len(valid_weights) < n_simulations:
        return generate_valid_weights(n_assets, n_simulations)
    
    # Take exactly n_simulations weights
    return valid_weights[:n_simulations]

def get_stock_combinations(all_stocks: List[str], n_select: int = 25) -> List[Tuple[str, ...]]:
    """Generate combinations of n_select stocks from all_stocks.
    
    Args:
        all_stocks: List of all available stock symbols
        n_select: Number of stocks to select
        
    Returns:
        List of stock combinations
    """
    return list(combinations(all_stocks, n_select))

def evaluate_portfolio(returns_array: np.ndarray, weights: np.ndarray) -> Dict[str, float]:
    """Evaluate a portfolio using various metrics.
    
    Args:
        returns_array: NumPy array with daily returns
        weights: Array of portfolio weights
        
    Returns:
        Dictionary with portfolio metrics
    """
    return {
        'sharpe_ratio': calculate_sharpe_ratio(returns_array, weights),
        'annual_return': calculate_portfolio_return(returns_array, weights),
        'annual_volatility': calculate_portfolio_volatility(returns_array, weights)
    }

def find_best_portfolio_from_batch(
    returns_array: np.ndarray, 
    weights_batch: np.ndarray, 
    combination: Tuple[str, ...]
) -> Dict:
    """Find the best portfolio from a batch of weights using vectorized operations."""
    # Calculate metrics for all weights using vectorized operations
    sharpe_ratios, returns, volatilities = calculate_portfolio_metrics_vectorized(
        returns_array, weights_batch
    )
    
    # Find the index with the maximum Sharpe ratio
    best_idx = np.argmax(sharpe_ratios)
    
    # Convert to Python types for JSON serialization
    weights_dict = {stock: float(weight) for stock, weight in zip(combination, weights_batch[best_idx])}
    
    return {
        'stocks': list(combination),
        'weights': weights_dict,
        'sharpe_ratio': float(sharpe_ratios[best_idx]),
        'annual_return': float(returns[best_idx]),
        'annual_volatility': float(volatilities[best_idx])
    } 