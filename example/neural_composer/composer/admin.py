# coding: utf-8

from django.contrib import admin
from django.core.urlresolvers import reverse

from models import Song


class SongAdmin(admin.ModelAdmin):
    list_display = ['key', 'is_composed', 'created_at', 'url']

    def url(self, obj):
        return '<a href="{}" target="_blank">Link</a>'.format(reverse('composer_song', kwargs={'key': obj.key}))

    url.allow_tags = True

admin.site.register(Song, SongAdmin)
