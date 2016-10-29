# coding: utf-8

import os
import random
import hashlib

from django.db import models

from settings import SONG_STORE_PATH

from django.conf import settings


class Song(models.Model):
    KEY_LENGTH = 10

    key = models.CharField(max_length=10, unique=True, verbose_name=u'уникальный ключ песни')
    song = models.TextField(blank=True, null=True, verbose_name=u'песня')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'дата создания')

    def __unicode__(self):
        return self.key

    @classmethod
    def create(cls):
        key = hashlib.md5(str(random.random())).hexdigest()[:cls.KEY_LENGTH]

        song = Song(key=key)
        song.save()

        return song

    @property
    def is_composed(self):
        return bool(self.song)

    @property
    def store_path(self):
        return os.path.join(SONG_STORE_PATH, self.created_at.strftime('%Y-%m-%d'), self.key)

    @property
    def mp3_file(self):
        return os.path.join(self.store_path, 'song.mp3')

    @property
    def midi_file(self):
        return os.path.join(self.store_path, 'song.mid')

    @property
    def mp3_media(self):
        return self.mp3_file.replace(SONG_STORE_PATH, settings.MEDIA_URL)
