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
        if i < self.width:
            return [50.0]

        delta = np.array([self.feature.calc(ds, i)[0] for i in range(i - self.width, i+1)])
        delta = np.diff(delta)

        up, down       = delta.copy(), delta.copy()
        up[up < 0]     = 0
        down[down > 0] = 0

        rol_up   = pd.rolling_mean(up, self.width)
        rol_down = pd.rolling_mean(down, self.width)
        rol_down = np.absolute(rol_down)
        
        rs = rol_up / rol_down
        
        rsi = 100 - ( 100 / ( 1 + rs ) )

        return [(rsi[self.width - 1] * 0.0001) + 1.2]

    def plot(self, p, ds, a, b, color='b', is_pred=False):
        self.feature.plot(p, ds, a, b, color, is_pred)