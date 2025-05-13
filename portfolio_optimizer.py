import numpy as np
import pandas as pd
from typing import List, Tuple, Dict
from multiprocessing import Pool, cpu_count
from utils import (
    calculate_daily_returns,
    generate_valid_weights,
    get_stock_combinations,
    find_best_portfolio_from_batch
)

def process_stock_combination(
    combination: Tuple[str, ...],
    returns_array: np.ndarray,
    column_indices: List[int],
    n_simulations: int = 1000
) -> Dict:
    """Process a single stock combination with vectorized operations."""
    try:
        # Get returns for selected stocks using numpy indexing (much faster)
        selected_returns = returns_array[:, column_indices]
        
        # Generate valid weights as a batch
        weights_batch = generate_valid_weights(len(combination), n_simulations)
        
        # Find the best portfolio using vectorized operations
        return find_best_portfolio_from_batch(selected_returns, weights_batch, combination)
    except Exception as e:
        print(f"Error in process_stock_combination: {e}")
        return None

def process_combinations_chunk(args):
    """Process a chunk of combinations."""
    try:
        combinations_chunk, returns_array, column_map, n_simulations = args
        results = []
        
        # Process each combination
        for combination in combinations_chunk:
            try:
                # Get column indices for this combination
                indices = [column_map[stock] for stock in combination]
 
                # Process the combination
                result = process_stock_combination(combination, returns_array, indices, n_simulations)
                if result is not None:
                    results.append(result)
            except Exception as e:
                print(f"Error processing combination {combination}: {e}")
                continue
        
        return results
    except Exception as e:
        print(f"Error in process_combinations_chunk: {e}")
        return []

def optimize_portfolio(
    prices: pd.DataFrame,
    n_select: int = 25,
    n_simulations: int = 1000,
    n_workers: int = None,
    chunk_size: int = None
) -> Dict:
    """Optimize portfolio using parallel processing with chunking."""
    # Set number of workers if not specified
    if n_workers is None:
        n_workers = max(1, cpu_count() - 1)  # Leave one CPU free
    
    try:
        returns = calculate_daily_returns(prices)
        returns_array = returns.values
        
        column_map = {stock: i for i, stock in enumerate(returns.columns)}
        
        # Get all stock combinations
        all_stocks = prices.columns.tolist()
        combinations = get_stock_combinations(all_stocks, n_select)
        print(f"Generated {len(combinations)} combinations")
        
        # Determine optimal chunk size if not specified
        if chunk_size is None:
            # Use a formula based on CPU count and combinations count
            total_combinations = len(combinations)
            # Aim for ~3-4 chunks per worker for better load balancing
            chunks_per_worker = 4
            chunk_size = max(1, total_combinations // (n_workers * chunks_per_worker))
            # Limit maximum chunk size
            chunk_size = min(chunk_size, 250)
            print(f"Using auto-calculated chunk size: {chunk_size}")
        
        # Split combinations into chunks
        n_chunks = max(1, len(combinations) // chunk_size)
        chunks = np.array_split(combinations, n_chunks)
        print(f"Processing in {len(chunks)} chunks using {n_workers} workers")
        
     
        
        # Process combinations in parallel with chunks
        with Pool(processes=n_workers, maxtasksperchild=100) as pool:
            chunk_results = pool.map(process_combinations_chunk, [(chunk, returns_array, column_map, n_simulations) for chunk in chunks])
        
        # Flatten results and filter out None
        results = [portfolio for chunk in chunk_results for portfolio in chunk if portfolio is not None]
        
        if not results:
            raise ValueError("No valid portfolios found. All combinations failed.")
        
        # Find best portfolio
        best_portfolio = max(results, key=lambda x: x['sharpe_ratio'])
        
        return best_portfolio
    
    except Exception as e:
        print(f"Error in optimize_portfolio: {e}")
        raise 

def optimize_portfolio_sequential(
    prices: pd.DataFrame,
    n_select: int = 25,
    n_simulations: int = 1000
) -> Dict:
    """Optimize portfolio using sequential processing."""
    try:
        returns = calculate_daily_returns(prices)
        returns_array = returns.values
        
        column_map = {stock: i for i, stock in enumerate(returns.columns)}
        
        # Get all stock combinations
        all_stocks = prices.columns.tolist()
        combinations = get_stock_combinations(all_stocks, n_select)
        print(f"Generated {len(combinations)} combinations")
        
        results = []
        # Process each combination sequentially
        for combination in combinations:
            try:
                # Get column indices for this combination
                indices = [column_map[stock] for stock in combination]
                
                # Process the combination
                result = process_stock_combination(combination, returns_array, indices, n_simulations)
                if result is not None:
                    results.append(result)
            except Exception as e:
                print(f"Error processing combination {combination}: {e}")
                continue
        
        if not results:
            raise ValueError("No valid portfolios found. All combinations failed.")
        
        # Find best portfolio
        best_portfolio = max(results, key=lambda x: x['sharpe_ratio'])
        
        return best_portfolio
    
    except Exception as e:
        print(f"Error in optimize_portfolio_sequential: {e}")
        raise 