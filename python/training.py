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
import time
from tensorflow.python.ops import rnn, rnn_cell

os.system('clear')

FILE = 'EURUSD_UTC_Ticks_Bid_2015.01.01_2015.01.02.csv'

df = pd.read_csv(FILE, parse_dates = [ 'Time' ], index_col = 'Time')
df.fillna(method = 'ffill')

ask = df[ 'Ask' ].resample('1Min').ohlc()
bid = df[ 'Bid' ].resample('1Min').ohlc()
ask['t'] = ask.index.map(matplotlib.dates.date2num)

old_value = 0
ask = ask[ 'open' ]
data = []

for res in ask.values:
	if math.isnan(res):
		res = old_value
	if res > old_value:
		data.append('up') # Up
	elif res == old_value:
		data.append('no') # No Move
	elif res < old_value:
		data.append('down') # Down
	old_value = res

#data = ask[ 'open' ]
data2 = data[:-100]
data = data[:len(data) - 100]

#-----------------------------------------

movements = ['up', 'no', 'down']
one_hot_cache = {}
for d in movements:
	i = movements.index(d)
	one_hot_cache[d] = [0]*i + [1] +  [0]*(len(movements)-i-1)

def one_hot_move(d):
	return one_hot_cache[d]

learning_rate = 0.001
training_iters = 500000
batch_size = 1000

n_inputs = 3
n_steps = len(data)
n_hidden = 128
n_classes = 3

x = tf.placeholder(tf.float32, [None, n_steps, n_inputs])
y = tf.placeholder(tf.float32, [None, n_classes])

weights = tf.Variable(tf.random_normal([n_hidden, n_classes]))
biases = tf.Variable(tf.random_normal([n_classes]))

def do_rnn(x, weights, biases):
	x = tf.transpose(x, [1, 0, 2])
	x = tf.reshape(x, [-1, n_inputs])
	x = tf.split(0, n_steps, x)

	lstm_cell = rnn_cell.BasicLSTMCell(n_hidden, forget_bias = 1.0)
	outputs, states = rnn.rnn(lstm_cell, x, dtype = tf.float32)

	return tf.matmul(outputs[-1], weights + biases)

pred = do_rnn(x, weights, biases)

cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y))
optimizer = tf.train.AdamOptimizer(learning_rate = learning_rate).minimize(cost)

correct_pred = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.initialize_all_variables()

sess = tf.Session()

sess.run(init)

sys.stdout.write('Training...\n')
sys.stdout.flush()
for i, _ in enumerate(range(training_iters)):
	sys.stdout.write('\r{0:.1f} % learned.'.format((i / training_iters) * 100))
	sys.stdout.flush()	

	batch_x = []
	batch_y = []

	for j in range(batch_size):
		k = i * batch_size + j
		if k + n_steps >= len(data):
			break

		xs = []
		for d in data[k:k+n_steps]:
			xs.append(one_hot_move(d))
		batch_x.append(xs)
		batch_y.append(one_hot_move(data[k + n_steps]))



	if len(batch_x) > 0:
		sess.run(optimizer, feed_dict={ x: batch_x, y: batch_y })

data3 = data2

while True:
	batch_x = []
	xs = []

	for d in data2:
		xs.append(one_hot_move(d))

	batch_x.append(xs)

	d_move = sess.run(tf.argmax(pred, 1), feed_dict = { x : batch_x })
	data2 = data2[1:]
	data2.append(movements[d_move[0]])
	#data3.append(movements[d_move[0]])
	sys.stdout.write('\n' + movements[d_move[0]])
	sys.stdout.flush()
	#time.sleep(0.1)

'''
X = ask
old_value = 0
data = []

for res in X.values:
	value = (res[0] + res[3]) * 0.5 # (Open + Close) / 2
	if math.isnan(value):
		value = old_value
	#print value
	if value > old_value:
		data.append([1,0,0]) # Up
	elif value == old_value:
		data.append([0,1,0]) # No Move
	elif value < old_value:
		data.append([0,0,1]) # Down
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
	batch_xs, batch_ys = [X, data]
	sess.run(train_step, feed_dict={ x : batch_xs, y_ : batch_ys })

correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

print('\n{0:.2f} % accuracy'.format((sess.run(accuracy, 
	feed_dict={ x : X, y_ : data})) * 100))

'''