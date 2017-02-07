#---------------------------------------
# IMPORTS
#---------------------------------------

from ask    import *
from bid    import *
from misc   import *
from onehot import *
from sma    import *
from volume import *

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def calc(ds, config):
    rows = []

    fts = []
    idx = 0
    for f in config.FEATURES:
        f.set_idx(idx)
        fts.append(f)
        idx += f.dim

    print "calculating features:", ", ".join([x.name for x in fts])

    for i in range(ds.num_rows):
        values = []

        for f in fts:
            values.extend(f.calc(ds, i))

        rows.append(findata.DataRow(values))

    return (idx, fts, findata.DataSet(rows))
