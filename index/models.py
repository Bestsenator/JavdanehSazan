import jdatetime
import os
from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.postgres.fields import ArrayField  # for save list
from uuid import uuid4
import random


def randomInt():
    return random.randint(123456, 999999)


def createSession():
    return '{}-{}'.format(uuid4(), uuid4())


def currentTime():
    dd = jdatetime.datetime.today()
    d = str(jdatetime.datetime.today())
    return dd


def uploadToDeveloper(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join('developer', filename)


def uploadToBook(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return os.path.join('book', filename)


class APIKEY(models.Model):
    Name = models.CharField(max_length=100, default=randomInt)
    ApiKey = models.TextField(default=createSession)
    RegisterTime = jmodels.jDateTimeField(default=currentTime)

    def __str__(self):
        return self.Name


class User(models.Model):
    langChoices = (
        (1, 'فارسی'),
        (2, 'عربی')
    )
    genderChoices = (
        (0, 'نامشخص'),
        (1, 'آقا'),
        (2, 'خانم')
    )
    Phone = models.CharField(max_length=11)
    Name = models.CharField(max_length=100)
    Family = models.CharField(max_length=100)
    Gender = models.IntegerField(default=0, choices=genderChoices)
    Email = models.CharField(max_length=100, blank=True, null=True)
    NationalCode = models.CharField(max_length=10, blank=True, null=True)
    Language = models.IntegerField(default=1, choices=langChoices)
    Session = models.TextField(default=createSession)


class Category(models.Model):
    ArbName = models.CharField(max_length=150, default='')
    PerName = models.CharField(max_length=150, default='')
    RegisterTime = jmodels.jDateTimeField(default=currentTime)

    def __str__(self):
        return self.ArbName + ' ' + self.PerName


class Wallet(models.Model):
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    Inventory = models.IntegerField(default=0)  # Toman
    PricePerCoin = models.IntegerField(default=0)  # Coin = Inventory / PricePerCoin


class VerifyCode(models.Model):
    Code = models.IntegerField(default=randomInt)
    Phone = models.CharField(max_length=11)
    isVerify = models.BooleanField(default=False)
    RegisterTime = jmodels.jDateTimeField(default=currentTime)


class Developers(models.Model):
    Name = models.CharField(max_length=100)
    Family = models.CharField(max_length=100)
    Expertise = models.CharField(max_length=100)
    Image = models.ImageField(upload_to=uploadToDeveloper, default='developer/default.png')
    RegisterTime = jmodels.jDateTimeField(default=currentTime)


class InfoProject(models.Model):
    AboutUs = models.TextField(max_length=2000)
    Contact = ArrayField(models.CharField(max_length=11), default=list)


class Request(models.Model):
    stChoices = (
        (0, 'WaitAccept'),
        (1, 'AcceptWithAdmin'),
        (2, 'SentSuggestion'),
        (3, 'Complete'),
        (-1, 'Canceled')
    )
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    Title = models.CharField(max_length=500)
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Content = models.TextField(max_length=2000)
    Status = models.IntegerField(default=0, choices=stChoices)
    DeadLine = jmodels.jDateTimeField(blank=True, null=True)
    RegisterTime = jmodels.jDateTimeField(default=currentTime)


class SuggestForRequest(models.Model):
    stChoices = (
        (0, 'WaitAccept'),
        (1, 'AcceptWithAdmin'),
        (2, 'Accept'),
        (-1, 'Reject')
    )
    Request = models.ForeignKey(Request, on_delete=models.CASCADE)
    User = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    Content = models.TextField(max_length=2000)
    Status = models.IntegerField(default=0, choices=stChoices)
    Price = models.IntegerField(default=0)
    RegisterTime = jmodels.jDateTimeField(default=currentTime)


class MiniBook(models.Model):
    Image = models.ImageField(upload_to=0)
    PageNumber = models.IntegerField(default=0)
    Author = models.CharField(default='', max_length=150)
    Rate = models.IntegerField(default=1)
    Publishers = models.TextField(max_length=200, default='')
    Counter = models.CharField(max_length=150)
    By = models.CharField(default='', max_length=150)


