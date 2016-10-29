# coding: utf-8

from __future__ import print_function

import os
import random

import numpy as np

from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM

from utils import sample
from settings import MODEL_CONF_DIR, MODEL_ARC_FILE, MODEL_ABC_DATA_PATH, MEMORY_LENGTH, MODEL_CHARS_PATH


learning_batch_size = 10**6
hidden_layer_size = 128
dropout_size = 0.2


song_list = []

with open(MODEL_ABC_DATA_PATH, 'r') as f:
    tmp_song = ''
    for line in f.readlines():
        if line.startswith('X:'):
            song_list.append(tmp_song.strip())
            tmp_song = ''

        tmp_song += line

song_list = song_list[1:]
print('song count:', len(song_list))

text = open(MODEL_ABC_DATA_PATH, 'r').read()
chars = sorted(list(set(text)))
open(MODEL_CHARS_PATH, 'w').write(''.join(chars))

char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

sentences = []
next_chars = []

for song in song_list:
    song = '#' * MEMORY_LENGTH + song + '$' * 7
    for _ in range(0, learning_batch_size / len(song_list)):
        start_index = random.randint(0, len(song) - MEMORY_LENGTH - 1)
        sentences.append(song[start_index:start_index + MEMORY_LENGTH])
        next_chars.append(song[start_index + MEMORY_LENGTH])

print('sentences count:', len(sentences))

X = np.zeros((len(sentences), MEMORY_LENGTH, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)

for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


print('building a model...')
model = Sequential()
model.add(LSTM(hidden_layer_size, return_sequences=True, input_shape=(MEMORY_LENGTH, len(chars))))
model.add(Dropout(dropout_size))
model.add(LSTM(hidden_layer_size, return_sequences=False))
model.add(Dropout(dropout_size))
model.add(Dense(len(chars)))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop')
model_path = '{}/h{}_m{}_d{}'.format(MODEL_CONF_DIR, str(hidden_layer_size), str(MEMORY_LENGTH), str(dropout_size))
os.mkdir(model_path)
open('{}/{}'.format(model_path, MODEL_ARC_FILE), 'w').write(model.to_json())


for iteration in range(1, 128):
    print('iteration:', iteration)
    model.fit(X, y, batch_size=128, nb_epoch=1)

    iteration_song_list = []
    for _ in range(10):
        diversity = random.randint(5, 10) / 10.0
        sentence = '#' * MEMORY_LENGTH + 'X:'
        sentence = sentence[-MEMORY_LENGTH:]
        generated = 'X:'

        while True:
            x = np.zeros((1, MEMORY_LENGTH, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1.

            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]

            sentence = sentence[-MEMORY_LENGTH + 1:] + next_char
            generated += next_char

            if len(generated) > 400 or generated.endswith('$$$'):
                break

        iteration_song_list.append(generated.rstrip('$'))

    model.save_weights('{}/model_weights_{}.h5'.format(model_path, iteration))
    with open('{}/songs_{}.txt'.format(model_path, iteration), 'w') as f:
        for song in iteration_song_list:
            f.write(song + '\n\n')
