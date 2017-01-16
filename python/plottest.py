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

'''
ask_vol =  df[ 'AskVolume' ].resample('1Min').sum()

plt.subplot(2, 1, 1)
ask[ 'close' ].plot()
plt.title('Ask (close)')
plt.xlabel('time')
plt.ylabel('value')

plt.subplot(2, 1, 2)
ask_vol.plot()
plt.title('Ask volume')
plt.xlabel('time')
plt.ylabel('value')

import warnings
warnings.filterwarnings('ignore')

df['20d_ma'] = pd.rolling_mean(df['Ask'], window=20)
df['50d_ma'] = pd.rolling_mean(df['Ask'], window=50)
df['bol_upper'] = pd.rolling_mean(df['Ask'], window=20) + 2 * pd.rolling_std(df['Ask'], 20, min_periods=20)
df['bol_lower'] = pd.rolling_mean(df['Ask'], window=20) - 2 * pd.rolling_std(df['Ask'], 20, min_periods=20)
df['20d_exma'] = pd.ewma(df['Ask'], span=20)
df['50d_exma'] = pd.ewma(df['Ask'], span=50)

df.plot(x=df.index, y=['Ask','20d_ma','bol_upper','bol_lower'])
plt.show()
'''