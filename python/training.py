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
TRESHOLD = 0.00001

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
	diff = res - old_value
	if abs(diff) < TRESHOLD:
		data.append('no') # Up
	elif diff <= -TRESHOLD:
		data.append('down') # No Move
	elif diff >= TRESHOLD:
		data.append('up') # Down
	old_value = res

#data = ask[ 'open' ]
data2 = data[-200:]
data = data[:len(data) - 200]

#-----------------------------------------

movements = ['up', 'no', 'down']
one_hot_cache = {}
for d in movements:
	i = movements.index(d)
	one_hot_cache[d] = [0]*i + [1] +  [0]*(len(movements)-i-1)

def one_hot_move(d):
	return one_hot_cache[d]

learning_rate = 0.001
training_iters = 2000
batch_size = 100

n_inputs = 3
n_steps = 100
n_hidden = 16
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
	sys.stdout.write('\r{0:.1f} % trained.'.format((i / training_iters) * 100))
	sys.stdout.flush()	

	batch_x = []
	batch_y = []

	for j in range(batch_size):
		k = (i % int(len(data) / batch_size)) * batch_size + j
		if k + n_steps >= len(data):
			break
		xs = []
		for d in data[k:k+n_steps]:
			xs.append(one_hot_move(d))
		batch_x.append(xs)
		batch_y.append(one_hot_move(data[k + n_steps]))

	if len(batch_x) > 0:
		sess.run(optimizer, feed_dict={ x: batch_x, y: batch_y })

data3 = data2[:100]


sys.stdout.write('\n\nTesting...\n')
sys.stdout.flush()

while len(data3) != len(data2):
	batch_x = []
	xs = []

	sys.stdout.write('\r{0:.1f} % tested.'.format(((len(data3) - 100) / (len(data2) - 100)) * 100))
	sys.stdout.flush()
	for d in data2[:100]:
		xs.append(one_hot_move(d))

	batch_x.append(xs)
	d_move = sess.run(tf.argmax(pred, 1), feed_dict = { x : batch_x })
	#data2 = data2[1:]
	#data2.append(movements[d_move[0]])
	data3.append(movements[d_move[0]])
	#sys.stdout.write('\n' + movements[d_move[0]])
	#sys.stdout.flush()
	#time.sleep(0.1)

data2 = data2[100:]
data3 = data3[100:]

corr = 0
fails = 0

for i in range(len(data3)):
	if data2[i] == data3[i]:
		corr += 1	
	else:
		fails += 1

print('\n\nAccuracy: {0:.1f} %'.format((corr / (corr + fails))* 100))
