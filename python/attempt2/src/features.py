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
    def __init__(self):
        pass

    def calc(self, ds, i):
        if i == 0:
            return 0.0

        a = ds.rows[i].close_ask
        b = ds.rows[i-1].close_ask

        return (a - b)/b

    def plot(self, ds, a, b):
        pass

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def calc(ds):
    rows = []

    fts = []
    for feature_name in config.FEATURES:
        fts.append(globals()[feature_name]())

    print "calculating features:", ", ".join(config.FEATURES)

    for i in range(ds.num_rows):
        values = []

        for f in fts:
            values.append(f.calc(ds, i))

        rows.append(findata.DataRow(values))

    return findata.DataSet(rows)
