import pandas as pd
import matplotlib.pyplot as plt

file_path = 'EURUSD_UTC_Ticks_Bid_2015.01.01_2015.01.02.csv'

df = pd.read_csv(file_path, parse_dates = [ 'Time' ], index_col = 'Time')
df.fillna(method = 'backfill')
print df.head()

df[ 'Bid' ].plot()
df[ 'Ask' ].plot()

ask =  df[ 'Ask' ].resample('1Min').ohlc()
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
