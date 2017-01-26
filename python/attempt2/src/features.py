#---------------------------------------
# IMPORTS
#---------------------------------------

import config
import csvdata
import findata
import numpy as np

#---------------------------------------
# CLASSES
#---------------------------------------

class CloseBid(object):
    def __init__(self, idx):
        self.idx = idx
        self.dim = 1

    def calc(self, ds, i):
        return [ds.rows[i].close_bid]

    def plot(self, p, ds, a, b, color):
        x1 = p.ds.rows[a].time
        y1 = ds.rows[a].raw[self.idx]

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = ds.rows[i].raw[self.idx]

            p.draw_line(x1, y1, x2, y2, color)

            x1, y1 = x2, y2


class Trend(object):
    def __init__(self, idx):
        self.idx = idx
        self.dim = 3

    def calc(self, ds, i):
        o = ds.rows[i].open_bid
        c = ds.rows[i].close_bid

        d = c - o

        if abs(d) < 0.000001:
            return [0, 1, 0]

        if c > o:
            return [0, 0, 1]

        return [1, 0, 0]

    def plot(self, p, ds, a, b, color='b'):
        x1 = p.ds.rows[a].time
        y1 = p.ds.rows[a].open_bid

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time

            t = ds.rows[i].raw[self.idx:self.idx+3]

            y2 = y1 + 0.0001 * (np.argmax(t)-1)

            p.draw_line(x1, y1, x2, y2, color)

            x1, y1 = x2, y2


class Change(object):
    def __init__(self, idx):
        self.idx = idx
        self.dim = 1

    def calc(self, ds, i):
        if i == 0:
            return [0.0]

        a = ds.rows[i].close_ask
        b = ds.rows[i-1].close_ask

        return [1000.0*(a - b)/b]

    def plot(self, p, ds, a, b, color='b'):
        x1 = p.ds.rows[a].time
        y1 = p.ds.rows[a].close_ask

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = y1 + ds.rows[i].raw[self.idx]/1000.0

            p.draw_line(x1, y1, x2, y2, color)

            x1, y1 = x2, y2

class SMA(object):
    def __init__(self, idx):
        self.idx = idx
        self.sma = 30
        self.dim = 1

    def calc(self, ds, i):
        n = 0
        avg = 0.0

        for i in range(i, i - self.sma, -1):
            if i < 0:
                break

            avg += ds.rows[i].close_bid
            n += 1

        return [100.0*avg / n]

    def plot(self, p, ds, a, b, color='b'):
        x1 = p.ds.rows[a].time
        y1 = ds.rows[a].raw[self.idx]/100.0

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = ds.rows[i].raw[self.idx]/100.0

            p.draw_line(x1, y1, x2, y2, color)

            x1, y1 = x2, y2

class RSI(object):
    def __init__(self, idx):
        self.idx = idx
        self.time_frame = 1

    def calc(self, ds, i):
        pass

    def plot(self, p, ds, a, b, color='b'):
        pass


#---------------------------------------
# FUNCTIONS
#---------------------------------------

def calc(ds):
    rows = []

    fts = []
    idx = 0
    for feature_name in config.FEATURES:
        f = globals()[feature_name](idx)
        fts.append(f)
        idx += f.dim

    print "calculating features:", ", ".join(config.FEATURES)

    for i in range(ds.num_rows):
        values = []

        for f in fts:
            values.extend(f.calc(ds, i))

        rows.append(findata.DataRow(values))

    return (idx, fts, findata.DataSet(rows))
