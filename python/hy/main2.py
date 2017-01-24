#!/usr/bin/env python

import matplotlib.pyplot as plt
import matplotlib
import numpy      as np
import pandas     as pd
import seq2seq
import sys
import tensorflow as tf

from matplotlib.finance import candlestick_ohlc

NUM_EPOCH = 1000000
WINDOW_SIZE = 20
OUT_WINDOW_SIZE = 5

import time


def calc_xs(xs):
    x = []

    for idx in range(len(xs)):
        x.append([xs[idx][3]])

    return x

def normalize_xs(xs):
    print "normalizing data..."

    x_min = 9999999
    x_max = -9999999

    for x in xs:
        for i in range(len(x)):
            value = x[i]
            if value < x_min:
                x_min = value

            if value > x_max:
                x_max = value

    amplitude = x_max - x_min

    for x in xs:
        for i in range(len(x)):
            x[i] = (x[i] - x_min) / amplitude

    x_min = 9999999
    x_max = -9999999

def calc_ys(xs):
    ys = []

    for idx in range(WINDOW_SIZE, len(xs)):
        ys.append([xs[idx - WINDOW_SIZE][0]])

    return ys

#def calc_y(x):
#    # threshold for no-change
#    t = 0.01
#
#    # close - open
#    d = x[3] - x[0]
#
#    if abs(d) <  t : return (1, 0, 0)
#    if d      < -t : return (0, 1, 0)
#    if d      >  t : return (0, 0, 1)
#
#    raise Exception("Invalid x value: {}".format(x))

def create_model():
    model = seq2seq.Seq2Seq(depth         = 1,
                            input_shape   = (WINDOW_SIZE, 1),
                            output_dim    = 1,
                            output_length = OUT_WINDOW_SIZE,
                            peek          = True)

    model.compile(loss="mse", optimizer="adam")

    return model

def plot_data(data, pred):
    fig, ax = plt.subplots()
    #fig.subplots_adjust(bottom=0.2)
    #ax.xaxis_date()

    #candlestick_ohlc(ax, quotes, width=0.0001)

    x = np.array(data.t[:,0])
    y = np.append(np.array(data.x[:,0]), np.array(data.z)[:,0])

    opx = x[0]
    opy = y[0]

    opx2 = x[-len(pred)]
    opy2 = pred[0]

    for i in range(1, len(x)):
        px = x[i]
        py = y[i]
        px2 = x[i]
        py2 = y[i] if i < len(data.x) else pred[i - len(data.x)]

        ax.plot((opx, px), (opy, py), color="b")

        if i >= len(y) - len(pred):
            ax.plot((opx2, px2), (opy2, py2), color="r")
            opx2 = px2
            opy2 = py2


        opx = px
        opy = py

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

    x = calc_xs(x)
    normalize_xs(x)

    data = lambda: None
    data.x = np.array(x)[:,:-1]
    data.y = calc_ys(data.x)
    data.t = np.array(x)[:,-1]

    return data

def load_data(fn):
    print "loading", fn

    df = pd.read_csv(fn, index_col="Time", parse_dates=["Time"])
    df = df.resample("1Min").ohlc()

    asks = df["Ask"].fillna(method="ffill")
    asks["time"] = asks.index.map(matplotlib.dates.date2num)

    x = [x for x in asks.values]
    x = calc_xs(x)
    normalize_xs(x)

    z = x[-60:]
    x = x[:-60]

    data = lambda: None
    data.x = np.array(x)
    data.y = calc_ys(data.x)
    data.z = np.array(z)
    data.t = np.reshape(np.array(asks["time"]), (len(asks["time"]), 1))

    return data


if __name__ == "__main__":
    print "initializing tensorflow"
    session = tf.Session()

    data = load_data("EURUSD_UTC_Ticks_Bid_2015.01.01_2015.01.02.csv")


    model = create_model()



    print "training..."

    it = 0
    itit=0
    while it < NUM_EPOCH:
        idx = itit % (len(data.x) - WINDOW_SIZE)
        itit+=1

        x = np.array([data.x[idx:idx+WINDOW_SIZE]])
        y = np.array([data.y[idx:idx+OUT_WINDOW_SIZE]])

        if len(x[0]) < WINDOW_SIZE or len(y[0]) < OUT_WINDOW_SIZE:
            itit = 0
            continue

        model.fit(x, y, nb_epoch=1)

        it += 1

        sys.stdout.write("\r{:.2f}%".format(100.0*it/NUM_EPOCH))
        sys.stdout.flush()


    pred = np.array([data.x[-WINDOW_SIZE:]])
    while len(pred[0]) < 60+WINDOW_SIZE:
        pp = np.array(pred[:,-WINDOW_SIZE:])

        #print pred
        #print
        #print pp
        #print "------"

        p = model.predict(pp, batch_size=WINDOW_SIZE)
        pred = np.append(pred, np.array(p), axis=1)
        print len(pred[0])


    plot_data(data, pred[0][-60:])



        #= model.predict(x, batch_size=WINDOW_SIZE, verbose=True)
