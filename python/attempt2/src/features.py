#---------------------------------------
# IMPORTS
#---------------------------------------

import config
import csvdata
import findata

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def calc(ds):
    rows = []

    print "calculating features:", ", ".join(config.FEATURES)

    for i in range(ds.num_rows):
        values = []

        for func in config.FEATURES:
            values.append(globals()[func](ds, i))

        rows.append(findata.DataRow(values))

    return findata.DataSet(rows)

def change(ds, i):
    if i == 0:
        return 0.0

    a = ds.rows[i].close_ask
    b = ds.rows[i-1].close_ask

    return (a - b)/b
