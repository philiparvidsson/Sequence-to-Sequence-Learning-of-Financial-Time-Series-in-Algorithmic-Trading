#---------------------------------------
# IMPORTS
#---------------------------------------

from features import *

#---------------------------------------
# CONSTANTS
#---------------------------------------

# NOTE: LAYERS FOR KERASLSTM MODEL
LAYERS = (128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128, 128)

# The number of samples to pass to the model on each training iteration.
BATCH_SIZE = 60

# Data resampling interval.
RESAMPLE = "1Min"

# Specifies which features to use.
FEATURES = [
    RelativeChange(CloseBid(), scale=10000.0),
    OneHotTrend(CloseBid(), threshold=0.000005),
    RelativeChange(SMA(CloseBid(), width=10), scale=10000.0),
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
INPUT_LENGTH = 60

# The output length, in number of data points. This is the number of data points
# to predict at a time.
OUTPUT_LENGTH = 60

# Maximum number of iterations to train.
TRAIN_ITERS = 1000000

# Maximum time to train, in minutes. Set to zero to disable time limit.
TRAIN_TIME = 1

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
