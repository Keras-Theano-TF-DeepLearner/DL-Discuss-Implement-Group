# coding: utf-8

import numpy as np


def sample(a, temperature):
    a = np.log(a) / temperature
    a = np.exp(a) / np.sum(np.exp(a))

    return np.argmax(np.random.multinomial(1, a, 1))
