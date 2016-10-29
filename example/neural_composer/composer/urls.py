# coding: utf-8

from django.conf.urls import url

import views


urlpatterns = [
    url(r'^$', views.index, name='composer_index'),
    url(r'^song/compose/$', views.compose_song, name='composer_compose_song'),
    url(r'^song/(?P<key>.+)/$', views.song, name='composer_song'),
]
