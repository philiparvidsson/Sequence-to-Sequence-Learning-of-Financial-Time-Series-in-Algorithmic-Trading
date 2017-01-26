#!/usr/bin/env python

#---------------------------------------
# IMPORTS
#---------------------------------------

import config
import csvdata
import features
import findata
import imp
import numpy as np
import plot
import sys
import time
import warnings

warnings.filterwarnings("ignore")

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def print_head(ds):
    print "showing first few lines of calculated features:"

    for i in range(5):
        print "    ", ds2.rows[i].raw

    print

def do_pred(model):
    pred = np.array(model.data[config.PRED_START-config.INPUT_LENGTH:config.PRED_START])

    while len(pred) < config.INPUT_LENGTH + config.PRED_LENGTH:
        p = model.predict(pred[-config.INPUT_LENGTH:])
        pred = np.concatenate((pred, p), axis=0)

    ds_pred = findata.DataSet([None for i in xrange(len(model.data))])

    for i in xrange(config.INPUT_LENGTH, len(pred)):
        ds_pred.rows[i - config.INPUT_LENGTH + config.PRED_START] = findata.DataRow(pred[i])

    return ds_pred

def present_results(fts, ds, ds2, model):
    pred = do_pred(model)

    c = ["#ff0000", "#00ff00", "#0000ff", "#ff7f00", "#7fff00", "#007fff", "#00ff7f", "#ff00ff"]
    legend = []

    if config.RESULTS == "plot":
        p = plot.Plot(ds)
        p.plot_ref()

        ci = 0
        for f in fts:
            c1 = c[ci % len(c)]
            ci += 1
            c2 = c[ci % len(c)]
            ci += 1

            f.plot(p, ds2, config.PRED_START, config.PRED_START + config.PRED_LENGTH, color=c1)
            f.plot(p, pred, config.PRED_START, config.PRED_START + config.PRED_LENGTH, color=c2)

            legend.append((c1, type(f).__name__))
            legend.append((c2, type(f).__name__ + " (pred)"))

        p.set_legend(legend)

        p.show()
    else:
        raise Exception("unknown results method: " + config.RESULTS)

#---------------------------------------
# ENTRY POINT
#---------------------------------------

if __name__ == "__main__":
    ds = csvdata.load("../data/EURUSD_UTC_Ticks_Bid_2015.01.01_2015.01.02.csv")
    dim, fts, ds2 = features.calc(ds)

    m = imp.load_source(config.MODEL, "models/" + config.MODEL + ".py")
    model = m.create_model(ds2, dim)

    print

    it = 0
    t = 0.0
    last_t = time.time()
    update_timer = 0.0
    while it < config.TRAIN_ITERS:
        it += 1

        dt = time.time() - last_t
        last_t = time.time()

        t += dt

        model.train_once()

        mins  = int(t/60.0)
        hours = int(mins/60.0)
        mins -= hours*60
        secs  = int(t - mins*60)

        update_timer += dt
        if update_timer >= 0.1:
            sys.stdout.write("\r training [{:02d}:{:02d}:{:02d}, {:.2f}%] ... ".format(hours, mins, secs, 100.0*it/config.TRAIN_ITERS))
            sys.stdout.flush()

            if config.TRAIN_TIME > 0 and t/60.0 > config.TRAIN_TIME:
                break

            update_timer = 0.0

    print

    present_results(fts, ds, ds2, model)
