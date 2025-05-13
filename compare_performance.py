import time
import pandas as pd
from portfolio_optimizer import optimize_portfolio, optimize_portfolio_sequential
from io_funcs import load_price_data

def print_portfolio_metrics(portfolio, prefix=""):
    """Print portfolio Sharpe ratio."""
    print(f"{prefix} Sharpe Ratio: {portfolio['sharpe_ratio']:.4f}")

def run_performance_comparison():
    # Load price data
    prices = load_price_data("data.csv")
    
    # Set parameters
    n_select = 25
    simulation_counts = [2, 10, 50, 100, 500, 1000]  # Test different numbers of simulations
    
    # Store results for summary table
    results = []
    
    for n_simulations in simulation_counts:
        print(f"\n{'='*20} Testing with {n_simulations} simulations {'='*20}")
        
        # Run sequential version
        print("\nRunning sequential optimization...")
        start_time = time.time()
        sequential_result = optimize_portfolio_sequential(prices, n_select, n_simulations)
        sequential_time = time.time() - start_time
        
        # Run parallel version
        print("\nRunning parallel optimization...")
        start_time = time.time()
        parallel_result = optimize_portfolio(prices, n_select, n_simulations)
        parallel_time = time.time() - start_time
        
        # Store results
        results.append({
            'simulations': n_simulations,
            'sequential_time': sequential_time,
            'parallel_time': parallel_time,
            'speedup': sequential_time/parallel_time,
            'sequential_sharpe': sequential_result['sharpe_ratio'],
            'parallel_sharpe': parallel_result['sharpe_ratio']
        })
        
        # Print performance comparison
        print("\nPerformance Comparison:")
        print("-" * 80)
        print(f"{'Simulations':^12} | {'Sequential Time (s)':^20} | {'Parallel Time (s)':^20} | {'Speedup Factor':^15}")
        print("-" * 80)
        print(f"{n_simulations:^12} | {sequential_time:^20.2f} | {parallel_time:^20.2f} | {sequential_time/parallel_time:^15.2f}x")
        
        # Print Sharpe ratios
        print_portfolio_metrics(sequential_result, "Sequential")
        print_portfolio_metrics(parallel_result, "Parallel")
        
        print("\n" + "="*60)
    
    # Print summary table
    print("\n\nSummary of All Results:")
    print("=" * 100)
    print(f"{'Simulations':^12} | {'Sequential Time (s)':^20} | {'Parallel Time (s)':^20} | {'Speedup Factor':^15} | {'Seq Sharpe':^12} | {'Par Sharpe':^12}")
    print("-" * 100)
    for r in results:
        print(f"{r['simulations']:^12} | {r['sequential_time']:^20.2f} | {r['parallel_time']:^20.2f} | {r['speedup']:^15.2f}x | {r['sequential_sharpe']:^12.4f} | {r['parallel_sharpe']:^12.4f}")
    print("=" * 100)

if __name__ == "__main__":
    run_performance_comparison()