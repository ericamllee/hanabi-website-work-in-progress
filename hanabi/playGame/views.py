# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def index(request):
  # name = request.POST['playername']
  # if (name == ""):
  #   return render(request, 'index.html', {'error_message': "You need to fill in a name"})
  # else: 
  #   return HttpResponseRedirect(reverse('game:join'))
  return render(request, 'playGame/join.html')

def play(request):
  return HttpResponse("You're playingn the game")

def join(request):
  return HttpResponse("You're going to join a game")
# Create your views here.
