# This is a tool for traders to analyze an S&P500 company and see if it is optimal for selling covered calls.
# IDEAL STRATEGY: Sell covered call if you are bullish, but the stock price won't go up in a month.
# MODEL: If the slope from the highest point to the current point is slightly negative, but you are bullish, then
#       covered calls are optimal

import pandas as pd
import random as rand
from twelvedata import TDClient

HTC_SLOPE_LOWER = -0.8
HTC_SLOPE_UPPER = -0.05

### Step 1: Find tickers ###

tickers_df = pd.read_csv("constituents_csv.csv")
random_index = rand.randint(0, len(tickers_df) - 1)
random_ticker = tickers_df["Symbol"][random_index]
print(f"Your random ticker is {random_ticker}.")

ticker = random_ticker

### Step 2: Make dataframe with chosen ticker ###

# Initialize client - apikey parameter is required
td = TDClient(apikey="key")

# Construct the necessary time series
ts = td.time_series(
    symbol=f"{ticker}",
    interval="1day",
    outputsize=365,
    timezone="America/New_York",
)
# Returns pandas.DataFrame
ts_df = ts.as_pandas()

### Step 3: Analyze data frame ###

# Find the highest tick, current tick and their slope.
highest_price = ts_df["high"].max()
highest_price_datetime = ts_df.index[ts_df["high"] == highest_price].date[0]

current_price = ts_df["close"].iloc[0]
current_price_datetime = ts_df.index[ts_df["close"] == current_price].date[0]

datetime_difference = current_price_datetime - highest_price_datetime
time_difference = datetime_difference.days

high_to_current_slope = (current_price - highest_price)/time_difference
if HTC_SLOPE_LOWER < high_to_current_slope < HTC_SLOPE_UPPER:
    print(f"{ticker}: PASS.")
else:
    print(f"{ticker}: FAIL.")
