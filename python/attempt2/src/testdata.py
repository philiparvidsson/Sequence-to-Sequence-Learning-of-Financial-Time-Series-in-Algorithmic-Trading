#---------------------------------------
# IMPORTS
#---------------------------------------

import config
import findata

import datetime
import matplotlib
import math
import numpy as np
import pandas as pd
import random

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def load_lineardata():
    print "generating linear data..."

    a = []
    t = []
    d = datetime.datetime(2015, 1, 1, 8, 0)
    y = 1.0
    while d < datetime.datetime(2015, 1, 1, 22, 0):
        g = random.random()+0.1
        r = 0.001*(random.random()-0.1)
        r1 = 0.001*random.random()
        r2 = 0.001*random.random()
        y += r*0.03
        d += datetime.timedelta(seconds=g)
        ask = 1.0 + y-r1
        bid = 1.0 + y+r2
        askvol = 5.0
        bidvol = 5.0

        t.append(d)
        a.append([ask, bid, askvol, bidvol])

    df = pd.DataFrame(np.array(a), index=np.array(t))
    df.columns = ["Ask", "Bid", "AskVolume", "BidVolume "]

    df_1min = df.resample(config.RESAMPLE)
    df_ohlc = df_1min.ohlc().fillna(method="ffill")
    df_vol  = df_1min.sum().fillna(method="ffill")
    df_time = df_ohlc.index.map(matplotlib.dates.date2num)

    rows = []

    for i in range(len(df_1min)):
        row = findata.DataRow([
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
        ])

        rows.append(row)


    return findata.DataSet(rows)

def load_sinedata(mul):
    print "generating sine data..."

    a = []
    t = []
    d = datetime.datetime(2015, 1, 1, 8, 0)
    x = 0
    while d < datetime.datetime(2015, 1, 1, 22, 0):
        r = 0.001*(random.random()-0.5)
        g = random.random()+0.1
        x += g*0.03
        d += datetime.timedelta(seconds=g)
        ask = 1.0 + math.sin(mul*x/80.0)*0.1+r
        bid = 1.0 + math.sin(mul*x/80.0+0.07)*0.1+r
        askvol = 5.0
        bidvol = 5.0

        t.append(d)
        a.append([ask, bid, askvol, bidvol])

    df = pd.DataFrame(np.array(a), index=np.array(t))
    df.columns = ["Ask", "Bid", "AskVolume", "BidVolume "]

    df_1min = df.resample(config.RESAMPLE)
    df_ohlc = df_1min.ohlc().fillna(method="ffill")
    df_vol  = df_1min.sum().fillna(method="ffill")
    df_time = df_ohlc.index.map(matplotlib.dates.date2num)

    rows = []

    for i in range(len(df_1min)):
        row = findata.DataRow([
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
        ])

        rows.append(row)


    return findata.DataSet(rows)
