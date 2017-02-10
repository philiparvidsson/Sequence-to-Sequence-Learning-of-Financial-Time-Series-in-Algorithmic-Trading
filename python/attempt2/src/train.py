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

#config.TRAIN_TIME = 2

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
        print "    ", ds.rows[i].raw

    print

    print "showing min/max/avg for columns:"

    avgs = [0.0 for _ in ds.rows[0].raw]
    mins = [9999999.0 for _ in ds.rows[0].raw]
    maxs = [-9999999.0 for _ in ds.rows[0].raw]

    for i in range(ds.num_rows):
        r = ds.rows[i]
        for j in range(len(r.raw)):
            avgs[j] += r.raw[j] / ds.num_rows
            if r.raw[j] < mins[j]:
                mins[j] = r.raw[j]

            if r.raw[j] > maxs[j]:
                maxs[j] = r.raw[j]


    for i in range(len(avgs)):
        print "col", i, ":", "min={}, max={}, avg={}".format(mins[i], maxs[i], avgs[i])

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

    print_head(ds2)

    model = m.create_model(config, ds2, dim)

    print

    if config.TRAIN_TIME > 0:
        sys.stderr.write("will now run for {:.2f} hours".format(config.TRAIN_TIME/60.0))
        sys.stderr.write("\n")
        sys.stderr.flush()

    it = 0
    t = 0.0
    last_t = time.time()
    update_timer = 0.0
    save_timer = 0.0
    while config.TRAIN_TIME > 0 or it < config.TRAIN_ITERS:
        it += 1

        dt = time.time() - last_t
        last_t = time.time()

        t += dt

        model.train_once()

        mins  = int(t/60.0)
        hours = int(mins/60.0)
        secs  = int(t - mins*60)
        mins -= hours*60

        save_timer += dt
        if save_timer >= 600.0:
            model.save()
            save_timer = 0.0

        update_timer += dt
        if update_timer >= 1.0:
            if config.TRAIN_TIME > 0:
                sys.stderr.write("\r training [time={:02d}:{:02d}:{:02d}, iterations={}, epochs={}] ... ".format(hours, mins, secs, it, model.num_passes))
            else:
                sys.stderr.write("\r training [time={:02d}:{:02d}:{:02d}, iterations={}, epochs={}, {:.2f}%] ... ".format(hours, mins, secs, it, model.num_passes, 100.0*it/config.TRAIN_ITERS))
            sys.stderr.flush()

            if config.TRAIN_TIME > 0 and t/60.0 > config.TRAIN_TIME:
                sys.stdout.write(" training [time={:02d}:{:02d}:{:02d}, iterations={}, epochs={}] ... ".format(hours, mins, secs, it, model.num_passes))
                sys.stdout.flush()
                break

            update_timer = 0.0

    if config.TRAIN_TIME <= 0:
        sys.stdout.write(" training [time={:02d}:{:02d}:{:02d}, iterations={}, epochs={}] ... ".format(hours, mins, secs, it, model.num_passes))
        sys.stdout.flush()

    print

    model.save(True)
    r.present(do_pred(model), fts, ds, ds2, model, config)
