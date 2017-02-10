#---------------------------------------
# IMPORTS
#---------------------------------------

import keras
import numpy as np
import os

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def create_model(config, ds, dim):
    print "creating keraslstm model..."

    model = keras.models.Sequential()

    Activation = keras.layers.core.Activation
    LSTM       = keras.layers.recurrent.LSTM
    Dense      = keras.layers.core.Dense
    Dropout    = keras.layers.core.Dropout
    Softmax    = keras.layers.core.Activation

    model.add(LSTM(input_dim=dim, output_dim=config.LAYERS[0], return_sequences=True))
    model.add(Dropout(0.2))

    for i in range(1, len(config.LAYERS)):
        model.add(LSTM(config.LAYERS[i], return_sequences=True))
        model.add(Dropout(0.2))

    model.add(Dense(output_dim=dim))
    #model.add(Activation("softmax"))

    model.compile(loss="mean_squared_error", optimizer="rmsprop")
    model.summary()

    model.data = np.array(ds.to_array()[:config.PRED_START])
    model.idx = 0
    model.num_passes = 0

    pred = model.predict
    def predict(x):
        x = np.array([x])
        return np.array(pred(x)[0][:config.OUTPUT_LENGTH])

    old_save = model.save
    def save(is_final=False):
        fn = os.path.join("..", "out", config.__name__ + ".h5")
        fnbak = fn + ".bak"

        if os.path.isfile(fn):
            if os.path.isfile(fnbak):
                os.remove(fnbak)

            os.rename(fn, fnbak)

        old_save(fn)
        if is_final and os.path.isfile(fnbak):
            os.remove(fnbak)

    def train_once():
        x = []
        y = []

        idx = model.idx

        for i in xrange(config.BATCH_SIZE):
            a = model.idx
            b = a + config.INPUT_LENGTH
            c = b + config.INPUT_LENGTH

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

    model.predict = predict
    model.save = save
    model.train_once = train_once

    return model
