from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from .models import User,Income,Expense
from django.db import IntegrityError
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from json import dumps
def testfunction(request):
    #this funtion was used for various debugging things during development
    # User.objects.all().delete()

    users = User.objects.all()
    for user in users:
        print(user.username,user.password)
    return HttpResponse('this is a test function')


def signup(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        cnf_pass = request.POST['cnf-pass']
        if password == cnf_pass:
            print(username,password)
            #attempt to create a new user
            try:
                user = User.objects.create_user(username=username, password=password)
                login(request,user)
                #add the reverse route here
            except IntegrityError:
                return render(request, "capstone/signup.html", {
                    "message": "Username already taken."
                })
            # print(User.objects.get(username = username))


        else: 
            return render(request,"capstone/signup.html",{
                "message":'Passwords are not the same, Try again',

            })


    return render(request,"capstone/signup.html")

def login_view(request):
    #login function
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user!=None:
            login(request,user)
            return HttpResponseRedirect(reverse('index'))

    else:
        return render(request,"capstone/login.html")     
        
           
def index(request):
    return render(request, 'capstone/index.html')

# Create your views here.


def get_data(request):
    data = {
        'sales': 100,
        'customers': 10,
    }
    data = dumps(data)
    return render(request,"capstone/index.html",{"data":data})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def transactions(request,rec_type):
    if rec_type == 'expense':
        trans_list = Expense.objects.all().filter(
            user = request.user ).order_by('id').reverse()
    
        return render(request, "capstone/transactions.html", {'trans': trans_list})
    elif rec_type == 'income':
        trans_list = Income.objects.all().filter(user=request.user).order_by('id').reverse()
        return render(request, "capstone/transactions.html", {'trans': trans_list})
        
def newentry(request):
    return render(request,"capstone/newentry.html")