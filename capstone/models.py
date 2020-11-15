from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass

class Income(models.Model):
    #model for income
    INC_CHOICES = (
        ('Salary', 'Salary'),
        ('Others', 'Others')
        
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    summary = models.CharField(max_length=128)
    inc_type = models.CharField(max_length=56, choices=INC_CHOICES)
    amt = models.IntegerField(default=0)

class Expense(models.Model):
    #model for expense
    EXP_CHOICES = (
        ('Food','Food'),
        ('Rent','Rent'),
        ('Entertainment','Entertainment'),
        ('Business', 'Business'),
        ('Travel','Travel'),
        ('Misc','Misc')
        
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    summary = models.CharField(max_length=128)
    exp_type = models.CharField(max_length=56, choices=EXP_CHOICES)
    amt = models.IntegerField(default=0)