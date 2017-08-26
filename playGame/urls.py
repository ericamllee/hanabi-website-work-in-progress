from django.conf.urls import url

from . import views

app_name = 'playGame'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'play', views.play, name="play"),
    url(r'join', views.join, name="join"),
]