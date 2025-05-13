# Portfolio Optimization Project
This project implements a Monte Carlo simulation approach to find the optimal wallet from the Dow Jones Index. The wallet is optimized for the Sharpe Ratio and contains 25 stocks of the 30 stocks in the Dow Jones Index.

## Project Description

The project implements a Monte Carlo simulation approach to find the optimal portfolio weights that maximize the Sharpe Ratio. The optimization is subject to the following constraints:
- Portfolio must be long-only
- No single asset can represent more than 20% of the portfolio
- The sum of all weights must equal 1 (100%)

## Requirements

- Python 3
- Required packages are listed in `requirements.txt`

## Installation

1. Clone this repository
2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the main script:
```bash
python main.py
```

The script will:
1. Load stock data for the second semester of 2024
2. Generate combinations of 25 stocks from the Dow Jones Index
3. For each combination, simulate 1,000 portfolio weightings
4. Calculate and optimize the Sharpe Ratio
5. Output the optimal portfolio weights and performance metrics

## Project Structure

- `main.py`: Main execution script
- `io_funcs.py`: Functions for input/output operations 
- `get_data.py`: Functions for fetching and loading data from Yahoo Finance
- `utils.py`: Utility functions for the project, mostly pure functions 
- `portfolio_optimizer.py`: Main logic for simulation
- `data.csv`: Sample data for the project
- `compare_performance.py`: Script for comparing the performance of the parallel and sequential optimization
- `testing.py`: Script for testing the results of the optimization with 2025 data

- `requirements.txt`: List of dependencies
- `README.md`: This file

## Expected Results

The program will output:
- The optimal combination of 25 stocks
- The optimal weights for each stock
- The achieved Sharpe Ratio
- Portfolio performance metrics (return and volatility)


## Functionality

### Data Fetching and Loading

The `io_funcs.py` module contains functions for fetching and loading data from Yahoo Finance.
The main script will start by checking if `data.csv` exists. If it does not exist, the script will fetch the data from Yahoo Finance and save it to `data.csv`.
The project includes a sample of the data in `data.csv` with data from the last semester of 2024. If you want to use your own data, you can do so by renaming
or deleting the `data.csv` file and running the script. You can also change the start and end dates of the data in the main script.

The main script then get information about your cpu and start the optimization process. The optimization process is implemented in the `portfolio_optimizer.py` module.
First the script will calculate the daily returns of the stocks this is done using pandas optimized function `pct_change()`. Then all combinations of 25 stocks are generated and the optimization process is started. 
The optimization process is parallelized for better performance. The combinations are grouped in chunks and processed in parallel by different workers. The number of chunks is automatically calculated based on the number of combinations and the number of workers. The number of workers is automatically calculated based on the number of cores in your cpu.

All the functions used in the parallelized sections are pure functions, with the exception of the weights generation. Altough it could be made pure by receiving the randomizer object as a parameter, this is pointless given that in python it is imported as a module. The seed is set to a constant value to ensure that the results are reproducible. It is necessary to have this function to run the simulation. 

For each chunk the task will iterate over all combinations and for each combination generate 1000 arrays of weights. Most of the project uses numpy vectorized operations for performance including for the weights generation.  Then for each weight array the sharpe ratio is calculated. The combination with the highest sharpe ratio is selected and returned. The data for the wallet is also saved to json file. 

The testing script will download data for 2025 and test the wallet metrics for the result of the optimization. 

The performance comparison script will run the optimization with different numbers of simulation comparing the performance of the parallel and sequential optimization. 

## Performance Comparison Results
This are results from the performance comparison script ran on a asus zephyrus g16 2024 laptop.
32 gb ram 
| Simulations | Sequential Time (s) | Parallel Time (s) | Speedup Factor | Seq Sharpe | Par Sharpe |
|------------|-------------------|------------------|----------------|------------|------------|
| 2          | 4.89              | 8.40             | 0.58x          | 2.4703     | 2.4278     |
| 10         | 5.35              | 8.33             | 0.64x          | 2.6562     | 2.6437     |
| 50         | 7.47              | 8.49             | 0.88x          | 2.6455     | 2.6580     |
| 100        | 10.14             | 8.81             | 1.15x          | 2.8374     | 2.8102     |
| 500        | 31.40             | 9.79             | 3.21x          | 2.8148     | 2.8673     |
| 1000       | 56.29             | 20.78            | 2.71x          | 2.8290     | 2.7893     |

### Analysis
 When generating just 2 weight array for each combination the parallel version is slower. This is likely due to the overhead of the parallel processing.
 For 10 and 50 simulations the parallel version is still slower but its speedup is higher.
 For 100 simulations the parallel version is faster and the speedup is 1.15x.
 For 500 simulations the speedup is 3.21x and for 1000 simulations the speedup is 2.71x.

The difference in speedup from 500 and 1000 simulations is not that big. The performance reduction for 1000 simulations could be caused by many different factors like resource constraints, for example ram and cache usage, it could also be just run to run varianced caused by cpu boost algorithms and other processes competing for resources.
 
## 2025 Data Results
The best wallet found with 2024 data had bad performance in 2025.
The sharpe ratio and annualized return were negative in 2025.
Q1 2025 Portfolio Metrics:
Sharpe Ratio: -0.5282
Annual Return: -0.0736
Annual Volatility: 0.1393

## Optional Improvements

 [ x ] Download data from api
 [ x ] Test with 2025 data
 [ x ] Compare with sequential optimization


 ## GEN AI Usage
Generative ai was used in this project in order to:
- Help generate some of the functions
- Improve perfomance optimizing existing code
- Generate Comments
