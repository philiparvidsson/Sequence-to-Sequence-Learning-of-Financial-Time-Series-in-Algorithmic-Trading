#---------------------------------------
# IMPORTS
#---------------------------------------

import config

import keras
import numpy as np

#---------------------------------------
# CONSTANTS
#---------------------------------------

LAYERS = (128, 128)

#---------------------------------------
# FUNCTIONS
#---------------------------------------

def create_model(ds, dim):
    print "creating keraslstm model..."

    model = keras.models.Sequential()

    Activation = keras.layers.core.Activation
    LSTM       = keras.layers.recurrent.LSTM
    Dense      = keras.layers.core.Dense
    Dropout    = keras.layers.core.Dropout
    Softmax    = keras.layers.core.Activation

    model.add(LSTM(input_dim=dim, output_dim=LAYERS[0], return_sequences=True))
    model.add(Dropout(0.2))

    for i in range(1, len(LAYERS)):
        model.add(LSTM(LAYERS[i], return_sequences=True))
        model.add(Dropout(0.2))

    model.add(Dense(output_dim=dim))
    #model.add(Activation("softmax"))

    model.compile(loss="mean_squared_error", optimizer="adam")
    model.summary()

    model.data = np.array(ds.to_array())
    model.idx = 0

    pred = model.predict
    def predict(x):
        x = np.array([x])
        return np.array(pred(x)[0][:config.OUTPUT_LENGTH])

    def train_once():
        x = []
        y = []

        idx = model.idx

        for i in xrange(config.BATCH_SIZE):
            a = model.idx
            b = a + config.INPUT_LENGTH
            c = b + config.INPUT_LENGTH

            model.idx += 1

            if c >= ds.num_rows:
                model.idx = 0
                continue

            x.append(model.data[a:b])
            y.append(model.data[b:c])

        model.idx = idx + 1

        x = np.array(x)
        y = np.array(y)

        model.fit(x, y, batch_size=config.BATCH_SIZE, nb_epoch=1, verbose=False)

    model.predict = predict
    model.train_once = train_once

    return model
