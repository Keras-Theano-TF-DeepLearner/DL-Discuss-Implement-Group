# coding: utf-8

import requests as r

from settings import MODEL_ABC_DATA_PATH


URL = 'https://thesession.org/tunes/{}/abc'
MAX_ID = 15240
wrong_line_set = {'Z:', 'S:', 'R:', 'L:'}


with open(MODEL_ABC_DATA_PATH, 'w') as f:
    for idx in range(1, MAX_ID):
        url = URL.format(idx)
        resp = r.get(url)
        if resp.status_code == 200:
            for line in resp.content.split('\n'):
                if not line[:2] in wrong_line_set:
                    f.write(line + '\n')
