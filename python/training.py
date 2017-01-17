#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
import tensorflow as tf
import sys
import math
import os

os.system('clear')

FILE = 'EURUSD_UTC_Ticks_Bid_2015.01.01_2015.01.02.csv'

df = pd.read_csv(FILE, parse_dates = [ 'Time' ], index_col = 'Time')
df.fillna(method = 'ffill')

ask = df[ 'Ask' ].resample('1Min').ohlc()
bid = df[ 'Bid' ].resample('1Min').ohlc()
ask['t'] = ask.index.map(matplotlib.dates.date2num)

X = ask
old_value = 0
yShite = []

for res in X.values:
	value = (res[0] + res[3]) * 0.5 # (Open + Close) / 2
	if math.isnan(value):
		value = old_value
	#print value
	if value > old_value:
		yShite.append([1,0,0]) # Up
	elif value == old_value:
		yShite.append([0,1,0]) # No Move
	elif value < old_value:
		yShite.append([0,0,1]) # Down
	old_value = value

# Create the model
x = tf.placeholder(tf.float32, [None, 5])
W = tf.Variable(tf.zeros([5, 3]))
b = tf.Variable(tf.zeros([3]))
y = tf.matmul(x, W) + b

# Define loss and optimizer
y_ = tf.placeholder(tf.float32, [None, 3])

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
training_iter = 100000

sess = tf.InteractiveSession()

tf.initialize_all_variables().run()

sys.stdout.write('Training...\n')
sys.stdout.flush()
for i, _ in enumerate(range(training_iter)):
	sys.stdout.write('\r{0:.1f} % learned.'.format((i / training_iter) * 100))
	sys.stdout.flush()
	batch_xs, batch_ys = [X, yShite]
	sess.run(train_step, feed_dict={ x : batch_xs, y_ : batch_ys })

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print('\n{0:.2f} % accuracy'.format((sess.run(accuracy, 
	feed_dict={ x : X, y_ : yShite})) * 100))

