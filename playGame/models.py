# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Game(models.Model):
  name = models.CharField(max_length=200)



  def __str__(self):
    return self.name


class Person(models.Model):
  name = models.CharField(max_length=200, unique=True)
  game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, blank=True, default=None)

  def __str__(self):
    return self.name + " " + self.game.__str__()


