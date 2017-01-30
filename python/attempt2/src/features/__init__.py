#---------------------------------------
# IMPORTS
#---------------------------------------

from ask    import *
from bid    import *
from volume import *

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
