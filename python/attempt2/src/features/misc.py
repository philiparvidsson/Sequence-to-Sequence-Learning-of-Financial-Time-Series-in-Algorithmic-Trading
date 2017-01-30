#---------------------------------------
# IMPORTS
#---------------------------------------

import numpy as np

#---------------------------------------
# CLASSES
#---------------------------------------

class RelativeChange(object):
    def __init__(self, feature, scale=1.0, hidden=False):
        assert feature.dim == 1
        self.hidden = hidden
        self.dim = 1
        self.feature = feature
        self.scale = scale
        self.name = "RelChange_" + feature.name

    def get_first_y(self, p, ds, i):
        return self.feature.get_first_y(p, ds, i)

    def set_idx(self, idx):
        self.idx = idx
        self.feature.set_idx(idx)

    def calc(self, ds, i):
        if i == 0:
            return [0.0]

        a = self.feature.calc(ds, i-1)[0]
        b = self.feature.calc(ds, i)[0]

        return [self.scale*(b-a)/a]

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        if self.hidden: return

        x1 = p.ds.rows[a].time
        y1 = self.feature.get_first_y(p, ds, a)

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = y1 + ds.rows[i].raw[self.idx]/self.scale

            p.draw_line(x1, y1, x2, y2, color, is_pred)

            x1, y1 = x2, y2
