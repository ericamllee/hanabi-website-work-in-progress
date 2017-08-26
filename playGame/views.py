# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from playGame.models import Person, Game
from django.db import IntegrityError


def index(request):
  if request.method == "GET":
    return render(request, 'playGame/index.html')
  elif request.method == "POST":
    if 'playername' in request.POST and request.POST['playername']:
      player_name = request.POST['playername']
      p = Person(name=player_name)
      #todo: make sure only one name at a time.
      try:
        p.save()
        return HttpResponseRedirect(reverse('playGame:join'))
      except IntegrityError:
        return render(request, 'playGame/index.html', {'error_message': player_name + " is already taken. Please enter a different name."})
    else:
      return render(request, 'playGame/index.html', {'error_message': "You need to fill in a name."})


def play(request):
  return render(request, 'playGame/play.html')


def join(request):
  if request.method == "GET":
    return render(request, 'playGame/join.html', {'people': getPeople()})
  elif request.method == "POST":
    player_list = request.POST.getlist('person')
    # print(request.POST)
    print(player_list)
    num_players = len(player_list)
    print(num_players)
    if 1 <= num_players <= 4:
      # todo: have a way to accept game requests from people.
      # todo: if more than one person accepts, then make a game and start it.
      return HttpResponseRedirect(reverse('playGame:play'))
    else:
      return render(request, 'playGame/join.html', {'error_message': "You must have between 2-4 players.", 'people': getPeople()})


    #todo: give it a parameter for the current player, and exclude the current player from the list.
def getPeople():
  return Person.objects.filter(game=None)

