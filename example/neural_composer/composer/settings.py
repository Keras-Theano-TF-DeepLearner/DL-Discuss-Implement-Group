# coding: utf-8

import os


MEMORY_LENGTH = 42

MAX_SONG_LENGTH = 300

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_CONF_DIR = os.path.join(BASE_DIR, 'model_conf')
MODEL_ARC_FILE = os.path.join(MODEL_CONF_DIR, 'model_arc.json')
MODEL_ABC_DATA_PATH = os.path.join(MODEL_CONF_DIR, 'session_abc_data.txt')
MODEL_CHARS_PATH = os.path.join(MODEL_CONF_DIR, 'chars.txt')

MODEL_ARC_PATH = os.path.join(MODEL_CONF_DIR, MODEL_ARC_FILE)
MODEL_WEIGHTS_PATH = os.path.join(MODEL_CONF_DIR, 'model_weights_34.h5')

SONG_STORE_PATH = '/var/composer/media/'
