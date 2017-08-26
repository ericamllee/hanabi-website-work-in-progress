from django.conf.urls import url

from . import views

app_name = 'playGame'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<player_id>[0-9]+)/play', views.play, name="play"),
    url(r'^(?P<player_id>[0-9]+)/join/', views.join, name="join"),
]