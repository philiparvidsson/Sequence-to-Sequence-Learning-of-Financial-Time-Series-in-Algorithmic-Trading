#---------------------------------------
# IMPORTS
#---------------------------------------

import numpy as np

#---------------------------------------
# CONSTANTS
#---------------------------------------

TREND_DOWN      = (1, 0, 0)
TREND_UNCHANGED = (0, 1, 0)
TREND_UP        = (0, 0, 1)

#---------------------------------------
# CLASSES
#---------------------------------------

class OneHotTrend(object):
    def __init__(self, feature, threshold=0.0001, hidden=False):
        assert feature.dim == 1
        self.hidden = hidden
        self.dim = 3
        self.feature = feature
        self.threshold = threshold
        self.name = "1HTrend_" + feature.name

    def set_idx(self, idx):
        self.idx = idx
        self.feature.set_idx(idx)

    def calc(self, ds, i):
        if i == 0:
            return TREND_UNCHANGED

        a = self.feature.calc(ds, i-1)[0]
        b = self.feature.calc(ds, i)[0]

        d = b - a

        if abs(d) < self.threshold:
            return TREND_UNCHANGED

        if b > a:
            return TREND_UP

        return TREND_DOWN

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        if self.hidden: return

        x1 = p.ds.rows[a].time
        y1 = self.feature.get_first_y(p, ds, a)

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time

            t = ds.rows[i].raw[self.idx:self.idx+3]

            y2 = y1 + 0.00005 * (np.argmax(t)-1)

            p.draw_line(x1, y1, x2, y2, color, is_pred)

            x1, y1 = x2, y2
