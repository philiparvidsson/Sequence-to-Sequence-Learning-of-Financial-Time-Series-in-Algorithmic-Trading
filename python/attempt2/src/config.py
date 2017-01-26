#---------------------------------------
# CONSTANTS
#---------------------------------------

# The number of samples to pass to the model on each training iteration.
BATCH_SIZE = 100

# Data resampling interval.
RESAMPLE = "1Min"

# Specifies which features to use (see featuers.py)
FEATURES = ["Change", "Trend", "CloseBid", "SMA"]

# The method to use to present the results.
# Methods:
#   plot - Plot the results to a graph.
RESULTS = "plot"

# The model to use for prediction.
MODEL = "farizrahman4u"

# The input length, in number of data points. This is the length of inputs
# passed to the RNN along the temporal axis.
INPUT_LENGTH = 20

# The output length, in number of data points. This is the number of data points
# to predict at a time.
OUTPUT_LENGTH = 5

# The number of layers to use in the model.
NUM_LAYERS = 1

# Maximum number of iterations to train.
TRAIN_ITERS = 10000

# Maximum time to train, in minutes. Set to zero to disable time limit.
TRAIN_TIME = 15

# The index in the aggregated data set to start predicting at. The model will be
# given access to the n data points before the prediction start, where n is
# INPUT_LENGTH.
PRED_START = -120

# The number of data points to predict.
PRED_LENGTH = 120
