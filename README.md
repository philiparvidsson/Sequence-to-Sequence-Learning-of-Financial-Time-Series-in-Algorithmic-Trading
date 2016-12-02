## bachelor-thesis

More info to come later!

## Compiling the document

Run `python make.py` in the project root directory. If you intend to work continuously on the thesis, run `python make.py watch` to have [pymake](https://github.com/philiparvidsson/pymake) automatically recompile the document when a change has been detected.

## Links

* https://student.portal.chalmers.se/sv/chalmersstudier/kandidat-och-examensarbete/examensarbete/Sidor/Planeringsrapport.aspx
* https://student.portal.chalmers.se/sv/chalmersstudier/kandidat-och-examensarbete/kandidatarbete/genomforande/Sidor/Planeringsrapport.aspx

* Writing a Thesis in LaTeX: https://www.sharelatex.com/blog/2013/08/02/thesis-series-pt1.html
* Trading and ML: https://www.youtube.com/playlist?list=PLAwxTw4SYaPnIRwl6rad_mYwEk4Gmj7Mx

## Lectures

* TensorFlow tutorial: https://www.youtube.com/watch?v=Ejec3ID_h0w&feature=youtu.be
* [Tensorflow and deep learning without a PhD, by Martin Görner](https://www.youtube.com/watch?v=vq2nnJ4g6N0)

## Delimitations:

* We will not be writing the source code for the neural networks. Instead, we will use [scikit-learn](http://scikit-learn.org/) and [TensorFlow](https://www.tensorflow.org/)
* We will only use FOREX data as source for financial data (other sources  do not provide real-time data)
* The problem will be treated as a classificatiom problem rather than a regression problem (maybe)

## Questions

### What is maximum drawdown?

Maximum drawdown is the ratio of the all-time high and all-time low prices of a stock:

`max_drawdown = (high - low)/high`

More info: https://www.youtube.com/watch?v=sgqQWb3tT6U

## Todo:

* Läsa om ANN & RNN, kanske LSTM
* Prova att implementera lite i TF