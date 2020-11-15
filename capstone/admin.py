from django.contrib import admin
# from django.contrib.auth.models import Group
from .models import User, Income,Expense

# Register your models here.
# admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Income)
admin.site.register(Expense)