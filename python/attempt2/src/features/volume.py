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

class VolumeAsk(object):
    def __init__(self, scale=1.0, hidden=False):
        self.scale = scale
        self.hidden = hidden
        self.dim = 1
        self.name = "VolAsk"

    def set_idx(self, idx):
        self.idx = idx

    def get_first_y(self, p, ds, i):
        return p.ds.rows[i].volume_ask*self.scale

    def calc(self, ds, i):
        return [ds.rows[i].volume_ask*self.scale]

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        if self.hidden: return

        x1 = p.ds.rows[a].time
        y1 = self.get_first_y(p, ds, a)

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = ds.rows[i].raw[self.idx]

            p.draw_line(x1, y1, x2, y2, color, is_pred)

            x1, y1 = x2, y2

class VolumeBid(object):
    def __init__(self, scale=1.0, hidden=False):
        self.scale = scale
        self.hidden = hidden
        self.dim = 1
        self.name = "VolBid"

    def set_idx(self, idx):
        self.idx = idx

    def get_first_y(self, p, ds, i):
        return p.ds.rows[i].volume_bid*self.scale

    def calc(self, ds, i):
        return [ds.rows[i].volume_bid*self.scale]

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        if self.hidden: return

        x1 = p.ds.rows[a].time
        y1 = self.get_first_y(p, ds, a)

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = ds.rows[i].raw[self.idx]

            p.draw_line(x1, y1, x2, y2, color, is_pred)

            x1, y1 = x2, y2
