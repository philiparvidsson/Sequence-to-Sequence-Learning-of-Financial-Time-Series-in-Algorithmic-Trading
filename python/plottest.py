#!/usr/bin/env python
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc

FILE = 'EURUSD_UTC_Ticks_Bid_2015.01.01_2015.01.02.csv'

df = pd.read_csv(FILE, parse_dates = [ 'Time' ], index_col = 'Time')
df.fillna(method = 'ffill')

ask = df[ 'Ask' ].resample('1Min').ohlc()
bid = df[ 'Bid' ].resample('1Min').ohlc()
ask['t'] = ask.index.map(matplotlib.dates.date2num)

fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
ax.xaxis_date()

try:
	candlestick_ohlc(ax, ask[['t', 'open', 'high', 'low', 'close']].values, width=0.0001)
except ValueError as e:
	print e
	print ask.shape

plt.xlabel('time')
plt.ylabel('value')
plt.show()