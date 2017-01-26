#---------------------------------------
# IMPORTS
#---------------------------------------

import config

import numpy as np
import seq2seq

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def create_model(ds, dim):
    model = seq2seq.Seq2Seq(depth         = config.NUM_LAYERS,
                            input_shape   = (config.INPUT_LENGTH, dim),
                            output_dim    = dim,
                            output_length = config.OUTPUT_LENGTH,
                            peek          = True)

    model.compile(loss="mse", optimizer="adam")

    model.data = np.array(ds.to_array())

    model.idx = 0

    pred = model.predict
    def predict(x):
        x = np.array([x])
        return np.array(pred(x)[0])

    def train_once():
        x = []
        y = []

        for i in xrange(config.BATCH_SIZE):
            a = model.idx
            b = a + config.INPUT_LENGTH
            c = b + config.OUTPUT_LENGTH

            model.idx += 1

            if c >= ds.num_rows:
                model.idx = 0

            x.append(model.data[a:b])
            y.append(model.data[b:c])

        x = np.array(x)
        y = np.array(y)

        model.fit(x, y, nb_epoch=1, verbose=False)

    model.predict    = predict
    model.train_once = train_once

    return model
