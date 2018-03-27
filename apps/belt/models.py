from __future__ import unicode_literals
from django.db import models
    
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Poke(models.Model):
    poker = models.ForeignKey(User, related_name="pokerpokes")
    poked = models.ForeignKey(User, related_name="pokedpokes")
    counter = models.IntegerField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    # added total with the hopes of making pokes on pokes.html work. need advice on this matter///total = models.IntegerField(default=0)
