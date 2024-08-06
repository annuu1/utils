import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to fetch historical data from Yahoo Finance
def fetch_data(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)
    df.reset_index(inplace=True)
    return df

# Function to detect support and resistance levels
def detect_support_resistance(df, window_size=20, threshold=0.01):
    # Calculate rolling max and min
    df['Rolling_Max'] = df['High'].rolling(window=window_size, center=True).max()
    df['Rolling_Min'] = df['Low'].rolling(window=window_size, center=True).min()

    # Identify local max (potential resistance) and local min (potential support)
    df['Is_Local_Max'] = (df['High'] == df['Rolling_Max'])
    df['Is_Local_Min'] = (df['Low'] == df['Rolling_Min'])

    resistance_levels = df[df['Is_Local_Max']]['High'].values
    support_levels = df[df['Is_Local_Min']]['Low'].values

    # Filter significant levels
    def filter_levels(levels, threshold=0.01):
        filtered_levels = []
        for level in levels:
            if not any(abs(level - l) < threshold for l in filtered_levels):
                filtered_levels.append(level)
        return filtered_levels

    significant_resistances = filter_levels(resistance_levels)
    significant_supports = filter_levels(support_levels)

    return significant_resistances, significant_supports

# Function to plot the data
def plot_data(df, significant_resistances, significant_supports):
    plt.figure(figsize=(14, 7))
    plt.plot(df['Date'], df['Close'], label='Close Price')
    plt.scatter(df[df['Is_Local_Max']]['Date'], df[df['Is_Local_Max']]['High'], color='red', label='Resistance', marker='^')
    plt.scatter(df[df['Is_Local_Min']]['Date'], df[df['Is_Local_Min']]['Low'], color='green', label='Support', marker='v')

    # Add significant levels
    for level in significant_resistances:
        plt.axhline(y=level, color='red', linestyle='--', label='Significant Resistance' if 'Significant Resistance' not in plt.gca().get_legend_handles_labels()[1] else "")
    for level in significant_supports:
        plt.axhline(y=level, color='green', linestyle='--', label='Significant Support' if 'Significant Support' not in plt.gca().get_legend_handles_labels()[1] else "")

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price with Support and Resistance Levels')
    plt.legend()
    plt.grid()
    plt.show()

# Main function to execute the workflow
def main():
    ticker = 'AAPL'  # Example: Apple Inc. Change this to the stock symbol you want to analyze
    start_date = '2023-01-01'
    end_date = '2024-01-01'

    # Fetch data
    df = fetch_data(ticker, start_date, end_date)

    # Detect support and resistance levels
    significant_resistances, significant_supports = detect_support_resistance(df)

    # Plot results
    plot_data(df, significant_resistances, significant_supports)

if __name__ == "__main__":
    main()
