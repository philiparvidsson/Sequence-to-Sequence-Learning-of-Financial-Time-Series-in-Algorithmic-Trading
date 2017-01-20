#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib
import numpy      as np
import pandas     as pd
import seq2seq
import sys
import tensorflow as tf

from matplotlib.finance import candlestick_ohlc

# Size of sliding window.
NUM_EPOCH = 100
WINDOW_SIZE = 3

def normalize_xs(xs):
    print "normalizing data..."

    x_min = 9999999
    x_max = -9999999

    for x in xs:
        for i in range(4):
            value = x[i]
            if value < x_min:
                x_min = value

            if value > x_max:
                x_max = value

    amplitude = x_max - x_min

    for x in xs:
        for i in range(4):
            x[i] = (x[i] - x_min) / amplitude

    x_min = 9999999
    x_max = -9999999


def calc_y(x):
    # threshold for no-change
    t = 0.01

    # close - open
    d = x[3] - x[0]

    if abs(d) <  t : return (1, 0, 0)
    if d      < -t : return (0, 1, 0)
    if d      >  t : return (0, 0, 1)

    raise Exception("Invalid x value: {}".format(x))

def create_model():
    model = seq2seq.Seq2Seq(depth         = 2,
                            input_shape   = (WINDOW_SIZE, 4),
                            output_dim    = 3,
                            output_length = WINDOW_SIZE,
                            peek          = True)

    model.compile(loss="mse", optimizer="sgd")

    return model

def plot_data(data):
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis_date()

    a = np.array(data.x)
    b = np.array(data.t)
    quotes = np.hstack((b,a))

    candlestick_ohlc(ax, quotes, width=0.0001)

    plt.xlabel('time')
    plt.ylabel('value')
    plt.show()

def load_test_data(fn):
    x = [[0.0, 0.0, 0.0, 0.0, 0.0],
         [0.1, 0.1, 0.1, 0.1, 0.1],
         [0.2, 0.2, 0.2, 0.2, 0.2],
         [0.3, 0.3, 0.3, 0.3, 0.3],
         [0.4, 0.4, 0.4, 0.4, 0.4],
         [0.5, 0.5, 0.5, 0.5, 0.5],
         [0.6, 0.6, 0.6, 0.6, 0.6],
         [0.7, 0.7, 0.7, 0.7, 0.7],
         [0.8, 0.8, 0.8, 0.8, 0.8],
         [0.9, 0.9, 0.9, 0.9, 0.9],
         [1.0, 1.0, 1.0, 1.0, 1.0]]

    normalize_xs(x)

    data = lambda: None
    data.x = np.array(x)[:,:-1]
    data.y = [calc_y(x) for x in data.x]
    data.t = np.array(x)[:,-1]

    return data

def load_data(fn):
    print "loading", fn

    df = pd.read_csv(fn, index_col="Time", parse_dates=["Time"])
    df = df.resample("1Min").ohlc()

    asks = df["Ask"].fillna(method="ffill")
    asks["time"] = asks.index.map(matplotlib.dates.date2num)

    x = [x for x in asks.values]
    normalize_xs(x)

    xx = np.array(x)

    data = lambda: None
    data.x = xx[:,:-1]
    data.y = [calc_y(x) for x in data.x]
    data.t = np.reshape(np.array(xx[:,-1]), (len(xx), 1))

    return data


if __name__ == "__main__":
    print "initializing tensorflow"
    session = tf.Session()

    data = load_data("EURUSD_UTC_Ticks_Bid_2015.01.01_2015.01.02.csv")

    plot_data(data)

    model = create_model()

    print "training..."

    it = 0
    while it < NUM_EPOCH:
        idx = it % (len(data.x) - WINDOW_SIZE)

        x = np.array([data.x[idx:idx+WINDOW_SIZE]])
        y = np.array([data.y[idx:idx+WINDOW_SIZE]])

        model.fit(x, y, nb_epoch=1)

        it += 1

        sys.stdout.write("\r{:.2f}%".format(100.0*it/NUM_EPOCH))
        sys.stdout.flush()
