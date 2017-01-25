
        model.fit(x, y, nb_epoch=1, verbose=False)

    model.predict    = predict
    model.train_once = train_once

    return model
