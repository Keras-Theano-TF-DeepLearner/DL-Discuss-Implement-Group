# coding: utf-8

import os

from django.shortcuts import redirect, render_to_response, get_object_or_404, RequestContext
from django.core.urlresolvers import reverse

import composer
import writer

from models import Song


def index(request):
    return render_to_response('composer/index.html', {
        'song_count': Song.objects.count()
    })


def compose_song(requset):
    song = composer.compose()
    return redirect(reverse('composer_song', kwargs={'key': song.key}))


def song(request, key):
    song = get_object_or_404(Song.objects.all(), key=key)
    if not os.path.isfile(song.mp3_file) and song.is_composed:
        writer.write(key)

    return render_to_response('composer/song.html', {
        'song': song,
    }, RequestContext(request))
