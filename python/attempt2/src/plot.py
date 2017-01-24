#---------------------------------------
# IMPORTS
#---------------------------------------

import findata

from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def plot(ds):
    fig, ax = plt.subplots()

    ax.xaxis_date()

    quotes = ds.transform(findata.TIME,
                          findata.OPEN_ASK,
                          findata.HIGH_ASK,
                          findata.LOW_ASK,
                          findata.CLOSE_ASK)

    candlestick_ohlc(ax, quotes, width=0.001)

    plt.show()
