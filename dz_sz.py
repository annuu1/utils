import yfinance as yf
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

# Fetch historical data for Bank Nifty
symbol = "^NSEBANK"
data = yf.download(symbol, start="2023-01-01", end="2024-12-31", interval="1d")

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

def check_zone_tested_and_target(demand_zone, candles, start_index):
    base_candles = demand_zone[2]
    highest_high = max(candle.high for candle in base_candles)
    lowest_low = min(candle.low for candle in base_candles)
    
    # Determine the target for a 1:2 risk-reward ratio
    risk = highest_high - lowest_low
    target_price = highest_high + 2 * risk

    for k in range(start_index, len(candles)):
        if candles[k].low <= highest_high and candles[k].high >= lowest_low:
            # Check if the price hits the 1:2 target after entering the zone
            for m in range(k, len(candles)):
                if candles[m].high >= target_price:
                    return 'pink'  # Zone achieved 1:2 target
                if candles[m].low < lowest_low:
                    return 'blue'  # Zone was broken before achieving target
            break
    
    return 'green'  # Zone has not been tested

# Convert fetched data to Candle objects
candles = []
for idx, row in data.iterrows():
    candles.append(Candle(row['Open'], row['High'], row['Low'], row['Close']))

# Detect demand zones
demand_zones = detect_demand_zones(candles)

# Track the number of fresh and tested zones
fresh_zones = 0
tested_zones = 0
target_zones = 0

# Prepare the plot and mark demand zones with horizontal rays
fig, ax = mpf.plot(data, type='candle', style='charles',
                   title='Bank Nifty with Detected Demand Zones',
                   ylabel='Price',
                   volume=False,  # Remove the volume
                   tight_layout=True,  # Remove the margin
                   show_nontrading=True,
                   returnfig=True)

# Add horizontal rays for demand zones
for dz in demand_zones:
    base_candles = dz[2]
    
    # Find the highest high and lowest low of the base candles
    highest_high = max(candle.high for candle in base_candles)
    lowest_low = min(candle.low for candle in base_candles)
    
    # Check if the zone has been tested and if it met the 1:2 target
    start_index = dz[1] + 1  # Start checking after the leg-out candle
    color = check_zone_tested_and_target(dz, candles, start_index)
    
    if color == 'green':
        fresh_zones += 1
    elif color == 'blue':
        tested_zones += 1
    elif color == 'pink':
        target_zones += 1
    
    # Add horizontal rays (lines) from these points extending to the right
    ax[0].hlines(y=highest_high, xmin=data.index[dz[0]], xmax=data.index[-1], color=color, linestyle='--', linewidth=1.5)
    ax[0].hlines(y=lowest_low, xmin=data.index[dz[0]], xmax=data.index[-1], color=color, linestyle='--', linewidth=1.5)

plt.show()

# Print the number of fresh, tested, and target zones
print(f"Number of fresh zones: {fresh_zones}")
print(f"Number of tested zones: {tested_zones}")
print(f"Number of zones that met 1:2 target: {target_zones}")
