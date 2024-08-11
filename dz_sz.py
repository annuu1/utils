import yfinance as yf
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

# Fetch historical data for Bank Nifty
symbol = "^NSEBANK"
data = yf.download(symbol, start="2023-01-01", end="2023-12-31", interval="1d")

# Convert data to a list of Candle objects
class Candle:
    def __init__(self, open_price, high, low, close):
        self.open_price = open_price
        self.high = high
        self.low = low
        self.close = close

    @property
    def body_size(self):
        return abs(self.close - self.open_price)

    @property
    def candle_range(self):
        return self.high - self.low

    @property
    def body_percentage(self):
        if self.candle_range == 0:
            return 0
        return (self.body_size / self.candle_range) * 100

    @property
    def is_bullish(self):
        return self.close > self.open_price

def is_legin_candle(candle):
    return candle.body_percentage > 60

def is_base_candle(candle):
    return candle.body_percentage < 45

def is_legout_candle(candle):
    return candle.body_percentage > 60

def detect_demand_zones(candles):
    demand_zones = []
    i = 0
    while i < len(candles) - 2:
        if is_legin_candle(candles[i]):
            base_candles = []
            j = i + 1
            while j < len(candles) and len(base_candles) < 5 and is_base_candle(candles[j]):
                base_candles.append(candles[j])
                j += 1

            if j < len(candles) and is_legout_candle(candles[j]):
                legin_candle = candles[i]
                legout_candle = candles[j]

                # Check if it's a demand zone
                if base_candles and (legout_candle.is_bullish and
                                     legout_candle.close > legin_candle.high and
                                     legout_candle.close > max(candle.high for candle in base_candles)):
                    demand_zones.append((i, j, base_candles))  # Store the indices and base candles
            i = j  # Skip to the next possible pattern after the legout candle
        else:
            i += 1

    return demand_zones

# Convert fetched data to Candle objects
candles = []
for idx, row in data.iterrows():
    candles.append(Candle(row['Open'], row['High'], row['Low'], row['Close']))

# Detect demand zones
demand_zones = detect_demand_zones(candles)

# Display detected demand zones
for dz in demand_zones:
    legin_index = dz[0]
    legout_index = dz[1]
    print(f"Demand zone detected from {data.index[legin_index]} to {data.index[legout_index]}")

# Prepare the plot and mark demand zones with horizontal rays
fig, ax = mpf.plot(data, type='candle', style='charles',
                   title='Bank Nifty with Detected Demand Zones',
                   ylabel='Price',
                   volume=True,
                   show_nontrading=True,
                   returnfig=True)

# Add horizontal rays for demand zones
for dz in demand_zones:
    base_candles = dz[2]
    
    # Find the highest open price of the base candles and the lowest low
    highest_open = max(candle.open_price for candle in base_candles)
    lowest_low = min(candle.low for candle in base_candles)
    
    # Add horizontal rays (lines) from these points extending to the right
    ax[0].hlines(y=highest_open, xmin=data.index[dz[0]], xmax=data.index[-1], color='green', linestyle='--', linewidth=1.5)
    ax[0].hlines(y=lowest_low, xmin=data.index[dz[0]], xmax=data.index[-1], color='green', linestyle='--', linewidth=1.5)

plt.show()
