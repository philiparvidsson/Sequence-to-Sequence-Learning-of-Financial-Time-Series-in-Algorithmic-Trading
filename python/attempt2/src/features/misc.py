#---------------------------------------
# IMPORTS
#---------------------------------------

import numpy as np

#---------------------------------------
# CLASSES
#---------------------------------------

class Spread(object):
    def __init__(self, feature1, feature2, hidden=False, scale=1.0):
        assert feature1.dim == 1
        assert feature2.dim == 1

        self.feature1 = feature1
        self.feature2 = feature2
        self.hidden = hidden
        self.scale = scale
        self.dim = 1
        self.name = "Spread_" + feature1.name + "_" + feature2.name

    def get_first_y(self, p, ds, i):
        return 0.5*(self.feature1.get_first_y(p, ds, i)+self.feature2.get_first_y(p, ds, i))

    def set_idx(self, idx):
        self.idx = idx
        self.feature1.set_idx(idx)
        self.feature2.set_idx(idx)

    def calc(self, ds, i):
        a = self.feature1.calc(ds, i)[0]
        b = self.feature2.calc(ds, i)[0]

        return [self.scale*(b-a)]

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        if self.hidden: return

        x1 = p.ds.rows[a].time
        y1 = self.get_first_y(p, ds, a)

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = ds.rows[i].raw[self.idx]+self.get_first_y(p, ds, a)

            p.draw_line(x1, y1, x2, y2, color, is_pred)

            x1, y1 = x2, y2


class RelativeChange(object):
    def __init__(self, feature, scale=1.0, hidden=False, plotscale=1.0):
        assert feature.dim == 1
        self.hidden = hidden
        self.dim = 1
        self.feature = feature
        self.scale = scale
        self.name = "RelChange_" + feature.name
        self.plotscale=plotscale

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

        if abs(a) < 0.00000000000001:
            return [0.0]

        return [self.scale*(b-a)/a]

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        if self.hidden: return

        x1 = p.ds.rows[a].time
        y1 = self.feature.get_first_y(p, ds, a)

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = y1 + self.plotscale*ds.rows[i].raw[self.idx]/self.scale

            p.draw_line(x1, y1, x2, y2, color, is_pred)

            x1, y1 = x2, y2
