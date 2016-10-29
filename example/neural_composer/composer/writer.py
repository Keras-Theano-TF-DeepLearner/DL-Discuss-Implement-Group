# coding: utf-8

import os

import celery
import music21

from models import Song


@celery.task
def write(song_key):
    song = Song.objects.get(key=song_key)

    score = music21.converter.parse(song.song)
    midi = music21.midi.translate.streamToMidiFile(score)

    if not os.path.exists(song.store_path):
        os.makedirs(song.store_path)

    midi.open(song.midi_file, 'wb')
    midi.write()
    midi.close()

    os.system('timidity -Ow -o - {} | lame - {}'.format(song.midi_file, song.mp3_file))
