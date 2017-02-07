#---------------------------------------
# IMPORTS
#---------------------------------------

import findata

from matplotlib.finance import candlestick_ohlc

import matplotlib
import matplotlib.pyplot as plt

import os

#---------------------------------------
# CLASSES
#---------------------------------------

class Plot(object):
    def __init__(self, ds):
        self.ds = ds
        self.fig = plt.figure(figsize=(100, 30))
        self.ax = self.fig.add_subplot(1, 1, 1)

        self.ax.xaxis_date()

        #plt.ion()

    def clear(self):
        self.ax.cla()

    def draw_line(self, x1, y1, x2, y2, color, is_pred=False):
        if is_pred:
            self.ax.plot((x1, x2), (y1, y2), color=color)
        else:
            self.ax.plot((x1, x2), (y1, y2), color=color, linestyle="dashed")

    def pause(self, t=0.0):
        plt.pause(t)

    def set_legend(self, legend):
        legend = [matplotlib.patches.Patch(color=x[0], label=x[1]) for x in legend]

        plt.legend(handles=legend, loc="lower left")

    def plot_ref(self):
        quotes = self.ds.transform(findata.TIME,
                                   findata.OPEN_ASK,
                                   findata.HIGH_ASK,
                                   findata.LOW_ASK,
                                   findata.CLOSE_ASK)

        candlestick_ohlc(self.ax, quotes, width=0.001, colorup='#e0ffe0', colordown='#ffe0e0')

    def show(self):
        plt.show()

    def save(self, fn):
        plt.savefig(fn)

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def present(pred, fts, ds, ds2, model, config):
    c = [
        "#ff0000",
        "#00ff00",
        "#0000ff",
        "#ff3f00",
        "#007fff",
        "#00ff7f",
        "#00e0e0",
        "#ff00ff",
        "#000000",
        "#606060",
        "#b0b0b0"
    ]

    legend = []


    p = Plot(ds)
    p.plot_ref()

    ci = 0
    for f in fts:
        if f.hidden:
            continue

        c1 = c[ci % len(c)]
        #ci += 1
        c2 = c[ci % len(c)]
        ci += 1

        f.plot(p, ds2, config.PRED_START, config.PRED_START + config.PRED_LENGTH, color=c1)
        f.plot(p, pred, config.PRED_START, config.PRED_START + config.PRED_LENGTH, color=c2, is_pred=True)

        legend.append((c1, f.name))
        #legend.append((c2, type(f).__name__ + " (pred)"))

    p.set_legend(legend)

    #p.show()
    p.save(os.path.join("..", "out", config.__name__ + ".png"))
