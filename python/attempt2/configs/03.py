#---------------------------------------
# IMPORTS
#---------------------------------------

from features import *

#---------------------------------------
# CONSTANTS
#---------------------------------------

# NOTE: LAYERS FOR KERASLSTM MODEL
# EACH ELEMENT IS THE NUMBER OF NEURONS IN THAT LAYER
LAYERS = (256, 128)

# The number of samples to pass to the model on each training iteration.
BATCH_SIZE = 60

# Data resampling interval.
RESAMPLE = "1Min"

# Specifies which features to use.
FEATURES = [
    RelativeChange(SMA(CloseBid(), width=5), scale=2500.0),
    RelativeChange(SMA(VolumeBid(), width=5), plotscale=0.001),
    RelativeChange(RSI(CloseBid(), width=5), scale=5.0, plotscale=0.1),
    RelativeChange(SMA(Spread(CloseBid(), CloseAsk()), width=5), scale=2.0, plotscale=0.001)
]

# The method to use to present the results.
# Methods:
#   plot - Plot the results to a graph.
RESULTS = "plot"

# The model to use for prediction. Please note that further (model specific)
# configuration is available in the model file!
MODEL = "keraslstm"

# The input length, in number of data points. This is the length of inputs
# passed to the RNN along the temporal axis.
INPUT_LENGTH = 10

# The output length, in number of data points. This is the number of data points
# to predict at a time.
OUTPUT_LENGTH = 1

# Maximum number of iterations to train.
TRAIN_ITERS = 10

# Maximum time to train, in minutes. Set to zero to disable time limit.
TRAIN_TIME = 10*60

# Indicates whether, after a single prediction step has been performed, the
# predicted data should be replaced with *real* data before being reinsrted into
# the next prediction attempt.  Setting this to True will give a better
# prediction, but, in a real trading scenario, limit the trader to predicting
# CONFIG_OUTPUT data points into the future.
PRED_REINSERT_REAL = True

# The index in the aggregated data set to start predicting at. The model will be
# given access to the n data points before the prediction start, where n is
# INPUT_LENGTH.
PRED_START = -120

# The number of data points to predict.
PRED_LENGTH = 120
