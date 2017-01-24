#---------------------------------------
# IMPORTS
#---------------------------------------

import config
import findata

import matplotlib
import pandas as pd

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def load(filename):
    print "loading dataset:", filename

    df = pd.read_csv(filename, index_col="Time", parse_dates=["Time"])
    df_1min = df.resample(config.RESAMPLE)
    df_ohlc = df_1min.ohlc()
    df_vol  = df_1min.sum()
    df_time = df_ohlc.index.map(matplotlib.dates.date2num)

    rows = []

    for i in range(len(df_1min)):
        row = findata.DataRow(
            df_time[i],
            df_ohlc["Ask"]["open"].values[i],
            df_ohlc["Bid"]["open"].values[i],
            df_ohlc["Ask"]["high"].values[i],
            df_ohlc["Bid"]["high"].values[i],
            df_ohlc["Ask"]["low"].values[i],
            df_ohlc["Bid"]["low"].values[i],
            df_ohlc["Ask"]["close"].values[i],
            df_ohlc["Bid"]["close"].values[i],
            df_vol["AskVolume"].values[i],
            df_vol["BidVolume "].values[i]
        )

        rows.append(row)


    return findata.DataSet(rows)
