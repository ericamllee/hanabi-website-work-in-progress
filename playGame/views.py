# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

def index(request):
  if request.method == "GET":
    return render(request, 'playGame/index.html')
  elif request.method == "POST":
    if 'playername' in request.POST and request.POST['playername']:
      return HttpResponseRedirect(reverse('playGame:join'))
    else:
      return render(request, 'playGame/index.html', {'error_message': "You need to fill in a name"})

def play(request):
  # return HttpResponse("You're playingn the game")
  return render(request, 'playGame/game.html')

def join(request):
  # return HttpResponse("You're going to join a game")
  return render(request, 'playGame/join.html')
# Create your views here.
