# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from playGame.models import Person

# todo: put this on the database
person_id = 5
names = [Person(name="Benny", id=1), Person(name="Tenny", id=2), Person(name="Renny", id=3), Person(name="Henny", id=4)]

def index(request):
  global person_id
  if request.method == "GET":
    return render(request, 'playGame/index.html')
  elif request.method == "POST":
    if 'playername' in request.POST and request.POST['playername']:
      names.append(Person(name=request.POST['playername'], id = person_id))
      person_id += 1
      return HttpResponseRedirect(reverse('playGame:join'))
    else:
      # todo: add name into names
      return render(request, 'playGame/index.html', {'error_message': "You need to fill in a name"})

def play(request):
  return render(request, 'playGame/game.html')

def join(request):
  return render(request, 'playGame/join.html', {'names': names})
