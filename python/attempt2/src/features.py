#---------------------------------------
# IMPORTS
#---------------------------------------

import config
import csvdata
import findata

#---------------------------------------
# CLASSES
#---------------------------------------

class Change(object):
    def __init__(self, idx):
        self.idx = idx

    def calc(self, ds, i):
        if i == 0:
            return 0.0

        a = ds.rows[i].close_ask
        b = ds.rows[i-1].close_ask

        return (a - b)/b

    def plot(self, p, ds, a, b, color='b'):
        x1 = p.ds.rows[a].time
        y1 = p.ds.rows[a].close_ask

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = y1 + ds.rows[i].raw[self.idx]

            p.draw_line(x1, y1, x2, y2, color)

            x1, y1 = x2, y2

class SMA(object):
    def __init__(self, idx):
        self.idx = idx
        self.SMA = 50

    def calc(self, ds, i):
        points = 0
        sum = 0
        
        for i in range(i, i - self.SMA, -1):
            if i < 0: 
                break

            sum += ds.rows[i].close_bid
            points += 1

        return sum / points

    def plot(self, p, ds, a, b, color='b'):
        x1 = p.ds.rows[a].time
        y1 = p.ds.rows[a].close_bid

        for i in xrange(a+1, b):
            x2 = p.ds.rows[i].time
            y2 = ds.rows[i].raw[self.idx]

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
        fts.append(globals()[feature_name](idx))
        idx += 1

    print "calculating features:", ", ".join(config.FEATURES)

    for i in range(ds.num_rows):
        values = []

        for f in fts:
            values.append(f.calc(ds, i))

        rows.append(findata.DataRow(values))

    return findata.DataSet(rows)
