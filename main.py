import numpy as np
import time
import multiprocessing
from datetime import datetime
from portfolio_optimizer import optimize_portfolio
from io_funcs import check_and_get_data, load_price_data, save_results, print_portfolio_summary

def main():
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Set date range
    start_date = "2024-08-01"
    end_date = "2024-12-31"
    data_path = "data.csv"
    
    # Check data and load if needed
    check_and_get_data(data_path, start_date, end_date)
    prices = load_price_data(data_path)
    print(prices)
    
    start_time = time.time()
    
    n_cores = multiprocessing.cpu_count()
    n_workers = max(1, n_cores - 1)  
    
    n_select = 25
    n_simulations = 1000
    
    # Optimize portfolio
    print("Optimizing portfolio...")
    best_portfolio = optimize_portfolio(
        prices=prices,
        n_select=n_select,
        n_simulations=n_simulations,
        n_workers=n_workers
    )
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    # Save results and print summary
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = save_results(best_portfolio, timestamp)
    print_portfolio_summary(best_portfolio, execution_time, results_file)

if __name__ == "__main__":
    main()