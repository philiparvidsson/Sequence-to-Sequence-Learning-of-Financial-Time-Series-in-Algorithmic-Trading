#---------------------------------------
# IMPORTS
#---------------------------------------

import findata

from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def plot_ref(ds):
    fig, ax = plt.subplots()

    ax.xaxis_date()

    quotes = ds.transform(findata.TIME,
                          findata.OPEN_ASK,
                          findata.HIGH_ASK,
                          findata.LOW_ASK,
                          findata.CLOSE_ASK)

    candlestick_ohlc(ax, quotes, width=0.001, colorup='#00ff00', colordown='#ff0000')

def show():
    plt.show()
