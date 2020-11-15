from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass

class Income(models.Model):
    #model for income
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    summary = models.CharField(max_length=128)
    inc_type = models.CharField(choices=['Salary','Others'])

class Expense(models.Model):
    #model for expense
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    summary = models.CharField(max_length=128)
    exp_type = models.CharField(choices=['Food','Rent','Entertainment','Business','Misc'])