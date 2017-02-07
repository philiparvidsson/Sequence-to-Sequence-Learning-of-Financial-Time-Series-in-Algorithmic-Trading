#!/usr/bin/env python

#---------------------------------------
# IMPORTS
#---------------------------------------

import imp
import os
import sys

#import config
# h4x0rz $upr3m3!!!
cname = os.path.splitext(os.path.basename(sys.argv[1]))[0]
config = imp.load_source(cname, sys.argv[1])

#config.TRAIN_TIME = 60*4

import csvdata
import features
import findata
import numpy as np
import testdata
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
    pred_in = np.array(model.data[config.PRED_START-config.INPUT_LENGTH:config.PRED_START])
    pred_out = np.array(model.data[config.PRED_START-config.INPUT_LENGTH:config.PRED_START])

    while len(pred_out) < config.INPUT_LENGTH + config.PRED_LENGTH:
        p = model.predict(pred_in[-config.INPUT_LENGTH:])

        if config.PRED_REINSERT_REAL:
            a = config.PRED_START-config.INPUT_LENGTH+len(pred_in)
            b = a + config.OUTPUT_LENGTH
            p2 = np.array(model.data[a:b])
            pred_in  = np.concatenate((pred_in , p2), axis=0)
        else:
            pred_in  = np.concatenate((pred_in , p), axis=0)

        pred_out = np.concatenate((pred_out, p), axis=0)

    ds_pred = findata.DataSet([None for i in xrange(len(model.data))])

    for i in xrange(config.INPUT_LENGTH, len(pred_out)):
        ds_pred.rows[i - config.INPUT_LENGTH + config.PRED_START] = findata.DataRow(pred_out[i])

    return ds_pred

#---------------------------------------
# ENTRY POINT
#---------------------------------------

if __name__ == "__main__":
    ds = csvdata.load(config, "../data/EURUSD_UTC_Ticks_Bid_2015.01.01_2015.01.02.csv")
    #ds = testdata.load_sinedata(3.0)
    dim, fts, ds2 = features.calc(ds, config)

    m = imp.load_source(config.MODEL  , os.path.join("models", config.MODEL) + ".py")
    r = imp.load_source(config.RESULTS, os.path.join("results", config.RESULTS) + ".py")

    print "config: ", config.__name__
    print "model: ", m.__name__
    print "results: ", r.__name__

    model = m.create_model(config, ds2, dim)

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
        secs  = int(t - mins*60)
        mins -= hours*60

        update_timer += dt
        if update_timer >= 1.0:
            sys.stdout.write("\r training [{:02d}:{:02d}:{:02d}, {}, {}, {:.2f}%] ... ".format(hours, mins, secs, it, model.num_passes, 100.0*it/config.TRAIN_ITERS))
            sys.stdout.flush()

            if config.TRAIN_TIME > 0 and t/60.0 > config.TRAIN_TIME:
                break

            update_timer = 0.0

    print

    model.save(os.path.join("..", "out", config.__name__ + ".h5"))
    r.present(do_pred(model), fts, ds, ds2, model, config)
