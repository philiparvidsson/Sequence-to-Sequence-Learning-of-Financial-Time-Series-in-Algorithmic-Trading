#---------------------------------------
# IMPORTS
#---------------------------------------

import config

import numpy as np
import seq2seq

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def create_model(ds):
    model = seq2seq.Seq2Seq(depth         = 2,
                            input_shape   = (config.INPUT_LENGTH, len(config.FEATURES)),
                            output_dim    = 1,
                            output_length = config.OUTPUT_LENGTH,
                            peek          = True)

    model.compile(loss="mse", optimizer="adam")

    model.data = np.array(ds.to_array())

    model.idx = 0

    def train_once():
        a = model.idx
        b = model.idx + config.INPUT_LENGTH
        c = b + config.OUTPUT_LENGTH

        x = np.array([model.data[a:b]])
        y = np.array([model.data[b:c]])

        model.idx += 1

        if c >= ds.num_rows:
            model.idx = 0

        model.fit(x, y, nb_epoch=1, verbose=False)

    model.train_once = train_once

    return model
