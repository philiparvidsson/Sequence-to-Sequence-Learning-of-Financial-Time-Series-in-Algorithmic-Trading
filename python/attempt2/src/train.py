#!/usr/bin/env python

#---------------------------------------
# IMPORTS
#---------------------------------------

import config
import csvdata
import features
import models
import plot
import sys
import time

#---------------------------------------
# IMPORTS
#---------------------------------------

#---------------------------------------
# ENTRY POINT
#---------------------------------------

if __name__ == "__main__":
    ds = csvdata.load("../data/EURUSD_UTC_Ticks_Bid_2015.01.01_2015.01.02.csv")
    ds2 = features.calc(ds)

    print "first few lines of calculated features"
    for i in range(5):
        print ds2.rows[i].raw

    model = models.farizrahman4u(ds2)

    t = 0.0
    last_t = time.time()
    sec_timer = 0.0
    for i in xrange(config.TRAIN_ITERS):
        dt = time.time() - last_t
        last_t = time.time()

        t += dt

        model.train_once()

        mins  = int(t/60.0)
        hours = int(mins/60.0)
        mins -= hours*60
        secs  = int(t - mins*60)

        sec_timer += dt
        if sec_timer >= 1.0:
            sys.stdout.write("\r training [{:02d}:{:02d}:{:02d}, {}/{}] ... ".format(hours, mins, secs, i, config.TRAIN_ITERS))
            sys.stdout.flush()
            sec_timer -= 1.0

            if config.TRAIN_TIME > 0 and t/60.0 > config.TRAIN_TIME:
                break

        model.train_once()

    if config.RESULTS == "plot":
        plot.plot(ds)
    else:
        raise Exception("unknown results method: " + config.RESULTS)
