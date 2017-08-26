# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Game(models.Model):
  name = models.CharField(max_length=200)

class Person(models.Model):
  name = models.CharField(max_length=200)
  game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True)

