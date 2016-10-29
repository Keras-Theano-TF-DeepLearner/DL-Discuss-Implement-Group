# coding: utf-8

import random
import numpy as np

import celery

from keras.models import model_from_json

from models import Song

import utils
import writer

from settings import MEMORY_LENGTH, MAX_SONG_LENGTH, MODEL_ARC_PATH, MODEL_CHARS_PATH, MODEL_WEIGHTS_PATH


class WriterException(Exception):
    pass


model = None


def get_model():
    global model

    if model is not None:
        return model

    model = model_from_json(open(MODEL_ARC_PATH, 'r').read())
    model.load_weights(MODEL_WEIGHTS_PATH)

    model.chars = set(open(MODEL_CHARS_PATH, 'r').read())
    model.char_indices = dict((c, i) for i, c in enumerate(model.chars))
    model.indices_char = dict((i, c) for i, c in enumerate(model.chars))

    return model


def compose():
    song = Song.create()
    compose_async.delay(song.key)
    return song


@celery.task
def compose_async(song_key):
    model = get_model()

    while True:
        diversity = random.uniform(0.7, 1.0)
        sentence = '#' * MEMORY_LENGTH + 'X:'
        sentence = sentence[-MEMORY_LENGTH:]
        generated = 'X:'

        while True:
            x = np.zeros((1, MEMORY_LENGTH, len(model.chars)))
            for t, char in enumerate(sentence):
                x[0, t, model.char_indices[char]] = 1.

            preds = model.predict(x, verbose=0)[0]
            next_index = utils.sample(preds, diversity)
            next_char = model.indices_char[next_index]

            sentence = sentence[-MEMORY_LENGTH + 1:] + next_char
            generated += next_char

            if generated.endswith('$$$'):
                try:
                    writer.write(song_key)

                    song = Song.objects.get(key=song_key)
                    song.song = generated.rstrip('$')
                    song.save()
                except WriterException:
                    break
                else:
                    return

            if len(generated) > MAX_SONG_LENGTH:
                break
