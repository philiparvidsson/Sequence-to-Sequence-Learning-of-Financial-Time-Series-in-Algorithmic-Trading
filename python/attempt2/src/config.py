#---------------------------------------
# IMPORTS
#---------------------------------------

from features import *

#---------------------------------------
# CONSTANTS
#---------------------------------------

# The number of samples to pass to the model on each training iteration.
BATCH_SIZE = 60

# Data resampling interval.
RESAMPLE = "1Min"

# Specifies which features to use.
FEATURES = [
	RSI(CloseBid(), width=28, hidden=True),
	
    RelativeChange(CloseBid(), scale=10000.0),
    SMA(RelativeChange(CloseBid(), scale=10000.0), width=10),

    RelativeChange(VolumeBid(), scale=0.01, hidden=True),
    SMA(RelativeChange(VolumeBid(), scale=0.01), width=10, hidden=True),
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
INPUT_LENGTH = 20

# The output length, in number of data points. This is the number of data points
# to predict at a time.
OUTPUT_LENGTH = 5

# Maximum number of iterations to train.
TRAIN_ITERS = 100000

# Maximum time to train, in minutes. Set to zero to disable time limit.
TRAIN_TIME = 5

# The index in the aggregated data set to start predicting at. The model will be
# given access to the n data points before the prediction start, where n is
# INPUT_LENGTH.
PRED_START = -600

# The number of data points to predict.
PRED_LENGTH = 120
