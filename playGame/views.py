# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from playGame.models import Person, Game


def index(request):
  if request.method == "GET":
    return render(request, 'playGame/index.html')
  elif request.method == "POST":
    if 'playername' in request.POST and request.POST['playername']:
      p = Person(name=request.POST['playername'])
      p.save()
      return HttpResponseRedirect(reverse('playGame:join'))
    else:
      return render(request, 'playGame/index.html', {'error_message': "You need to fill in a name"})


def play(request):
  return render(request, 'playGame/play.html')

def join(request):
  # todo: filter names for people not in games.
  if request.method == "GET":
    people = Person.objects.all()
    return render(request, 'playGame/join.html', {'people': people})
  elif request.method == "POST":
    if True:
      # todo: only allow 2-4 players in a game.
      # todo: have a way to accept game requests from people.
      return HttpResponseRedirect(reverse('playGame:play'))
    else:
      return render(request, 'playGame/join.html', {'error_message': "You must have between 2-4 players"})

