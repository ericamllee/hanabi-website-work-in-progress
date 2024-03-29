# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from playGame.models import Person, Game
from django.db import IntegrityError

#todo: make table empty out if someone leaves the website.

def index(request):
  if request.method == "GET":
    return render(request, 'playGame/index.html')
  elif request.method == "POST":
    if 'playername' in request.POST and request.POST['playername']:
      player_name = request.POST['playername']
      p = Person(name=player_name)
      try:
        p.save()
        return HttpResponseRedirect(reverse('playGame:join', args=(p.id,)))
      except IntegrityError:
        return render(request, 'playGame/index.html', {'error_message': "The name " + player_name + " is already taken. Please enter a different name."})
    else:
      return render(request, 'playGame/index.html', {'error_message': "You need to fill in a name."})


def play(request, player_id):
  return render(request, 'playGame/play.html')


def join(request, player_id):
  #todo: make page update every time the table changes.
  if request.method == "GET":
    return render(request, 'playGame/join.html', {'people': getPeople(player_id), 'player':player_id})
  elif request.method == "POST":
    player_list = request.POST.getlist('person')
    num_players = len(player_list)
    if 1 <= num_players <= 4:
      # todo: have a way to accept game requests from people.
      # todo: if more than one person accepts, then make a game and start it.
      g = Game(name=player_id)
      g.save()
      Person.objects.filter(pk=player_id).update(game=g)
      for player in player_list:
        Person.objects.filter(pk=player).update(game=g)
      return HttpResponseRedirect(reverse('playGame:play', args=(player_id,)))
    else:
      return render(request, 'playGame/join.html',
                    {'error_message': "Your game has " + (num_players + 1).__str__() +
                                      " players. The game must have 2-5 players.",
                     'people': getPeople(player_id), 'player':player_id})


def getPeople(person_id):
  return Person.objects.filter(game=None).exclude(id=person_id)

