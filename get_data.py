import yfinance as yf
import pandas as pd



def get_data(start_date, end_date):

    dow_30_tickers = [
        "AAPL", "AMGN", "AXP", "BA", "CAT", "CRM", "CSCO", "CVX", "DIS", "DOW",
        "GS", "HD", "HON", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "MMM",
        "MRK", "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA", "WMT"
    ]

    # Define the date range
    # start_date = "2024-08-01"
    # end_date = "2024-12-31"

    # Download historical data for all tickers
    data = yf.download(
        tickers=dow_30_tickers,
        start=start_date,
        end=end_date,
        interval="1d",
        group_by='ticker',
        auto_adjust=False,
        threads=True
    )

    # Initialize an empty list to hold individual DataFrames
    frames = []

    # Iterate over each ticker to process its data
    for ticker in dow_30_tickers:
        if ticker in data.columns.get_level_values(0):
            df = data[ticker].copy()
            df.reset_index(inplace=True)
            df['Ticker'] = ticker
            frames.append(df)

    # Concatenate all DataFrames into a single DataFrame
    merged_df = pd.concat(frames, ignore_index=True)

    # Save the merged DataFrame to a CSV file
    merged_df.to_csv("data.csv", index=False)

    print("Merged data saved to 'data.csv'")
