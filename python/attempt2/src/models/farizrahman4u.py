#---------------------------------------
# IMPORTS
#---------------------------------------

import numpy as np
import seq2seq

#---------------------------------------
# CONSTANTS
#---------------------------------------

NUM_LAYERS = 1

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def create_model(config, ds, dim):
    print "creating farizrahman4u model..."

    model = seq2seq.Seq2Seq(depth         = NUM_LAYERS,
                            input_shape   = (config.INPUT_LENGTH, dim),
                            output_dim    = dim,
                            output_length = config.OUTPUT_LENGTH,
                            peek          = True)

    model.compile(loss="mse", optimizer="rmsprop")

    model.data = np.array(ds.to_array()[:config.PRED_START])
    model.idx = 0
    model.num_passes = 0

    pred = model.predict
    def predict(x):
        x = np.array([x])
        return np.array(pred(x)[0])

    def train_once():
        x = []
        y = []

        idx = model.idx

        for i in xrange(config.BATCH_SIZE):
            a = model.idx
            b = a + config.INPUT_LENGTH
            c = b + config.OUTPUT_LENGTH

            model.idx += 1

            if c >= len(model.data):
                idx = -1
                model.idx = 0
                model.num_passes += 1
                continue

            x.append(model.data[a:b])
            y.append(model.data[b:c])

        model.idx = idx + 1

        x = np.array(x)
        y = np.array(y)

        model.fit(x, y, batch_size=config.BATCH_SIZE, nb_epoch=1, verbose=False)

    model.predict    = predict
    model.train_once = train_once

    return model
