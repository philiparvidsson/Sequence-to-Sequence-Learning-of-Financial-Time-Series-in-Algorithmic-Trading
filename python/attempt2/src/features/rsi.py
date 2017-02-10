#---------------------------------------
# IMPORTS
#---------------------------------------

import numpy as np
import pandas as pd

#---------------------------------------
# CLASSES
#---------------------------------------

class RSI(object):
    def __init__(self, feature, width=14, hidden=False):
        assert feature.dim == 1

        self.hidden  = hidden
        self.dim     = feature.dim
        self.feature = feature
        self.width   = width
        self.name    = "RSI" + str(width) + "_" + feature.name

    def set_idx(self, idx):
        self.idx = idx
        self.feature.set_idx(idx)

    def get_first_y(self, p, ds, i):
        return self.feature.get_first_y(p, ds, i)

    def calc(self, ds, i):
        #        if i < self.width:
        #            return [50.0]
        #
        #        delta = np.array([self.feature.calc(ds, i)[0] for i in range(i - self.width, i+1)])
        #        delta = np.diff(delta)
        #
        #        up, down       = delta.copy(), delta.copy()
        #        up[up < 0]     = 0
        #        down[down > 0] = 0
        #
        #        rol_up   = pd.rolling_mean(up, self.width)
        #        rol_down = pd.rolling_mean(down, self.width)
        #        rol_down = np.absolute(rol_down)
        #
        #        rs = rol_up / rol_down

        if i < 2:
            return [0.0]

        w = max(self.width, i)

        gt = 0.0
        lt = 0.0
        for j in range(1,w+1):
            d = self.feature.calc(ds, i-j)[0] - self.feature.calc(ds, i-j-1)[0]
            if d > 0.0:
                gt += d
            else:
                lt += abs(d)


        ag = gt / w
        al = lt / w
        rs = ag/al
        rsi = 100.0 - ( 100.0 / ( 1.0 + rs ) )

        return [rsi]

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        self.feature.plot(p, ds, a, b, color, is_pred)
