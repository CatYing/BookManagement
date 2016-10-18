# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class MyUser(models.Model):
    user = models.OneToOneField(User)
    nickname = models.CharField(max_length=64)

    def __unicode__(self):
        return self.nickname


class Author(models.Model):
    name = models.CharField(max_length=64)
    age = models.CharField(max_length=8, blank=True)
    country = models.CharField(max_length=32, blank=True)

    def __unicode__(self):
        return self.name


class Book(models.Model):
    ISBN = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=64, blank=True)
    author = models.ForeignKey(Author, blank=True, null=True)
    publisher = models.CharField(max_length=64, blank=True)
    publish_date = models.DateField(blank=True)
    price = models.CharField(max_length=32, blank=True)
    head_img = models.ImageField(upload_to='head_img/%Y/%m/%d')

    def __unicode__(self):
        return self.name




