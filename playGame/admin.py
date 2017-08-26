# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Game, Person

admin.site.register(Game)
admin.site.register(Person)