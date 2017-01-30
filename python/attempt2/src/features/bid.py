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

class RelCloseBid(object):
    def __init__(self, idx):
        self.idx = idx
        self.dim = 1
        self.mul = 10000.0

    def calc(self, ds, i):
        if i == 0:
            return [0.0]

        a = ds.rows[i].close_bid
        b = ds.rows[i-1].close_bid

        return [self.mul*(a - b)/b]

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        x1 = p.ds.rows[a].time
        y1 = p.ds.rows[a].close_bid

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = y1 + ds.rows[i].raw[self.idx]/self.mul

            p.draw_line(x1, y1, x2, y2, color, is_pred)

            x1, y1 = x2, y2

class RelHighBid(object):
    def __init__(self, idx):
        self.idx = idx
        self.dim = 1
        self.mul = 10000.0

    def calc(self, ds, i):
        if i == 0:
            return [0.0]

        a = ds.rows[i].high_bid
        b = ds.rows[i-1].high_bid

        return [self.mul*(a - b)/b]

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        x1 = p.ds.rows[a].time
        y1 = p.ds.rows[a].high_bid

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = y1 + ds.rows[i].raw[self.idx]/self.mul

            p.draw_line(x1, y1, x2, y2, color, is_pred)

            x1, y1 = x2, y2

class RelLowBid(object):
    def __init__(self, idx):
        self.idx = idx
        self.dim = 1
        self.mul = 10000.0

    def calc(self, ds, i):
        if i == 0:
            return [0.0]

        a = ds.rows[i].low_bid
        b = ds.rows[i-1].low_bid

        return [self.mul*(a - b)/b]

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        x1 = p.ds.rows[a].time
        y1 = p.ds.rows[a].low_bid

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = y1 + ds.rows[i].raw[self.idx]/self.mul

            p.draw_line(x1, y1, x2, y2, color, is_pred)

            x1, y1 = x2, y2

class RelOpenBid(object):
    def __init__(self, idx):
        self.idx = idx
        self.dim = 1
        self.mul = 10000.0

    def calc(self, ds, i):
        if i == 0:
            return [0.0]

        a = ds.rows[i].high_bid
        b = ds.rows[i-1].high_bid

        return [self.mul*(a - b)/b]

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        x1 = p.ds.rows[a].time
        y1 = p.ds.rows[a].high_bid

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = y1 + ds.rows[i].raw[self.idx]/self.mul

            p.draw_line(x1, y1, x2, y2, color, is_pred)

            x1, y1 = x2, y2
