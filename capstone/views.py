from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from .models import User,Income,Expense
from django.db import IntegrityError
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse
from json import dumps
from django.db.models import Sum

# this is what we use to create the dictionaried that we are making to senf to frontend
exp_type = ['Food','Rent','Entertainment','Business','Travel','Misc']
inc_type = ['Salary','Others']



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
    
    exp_dict = {}
    inc_dict = {}
    for key in exp_type:
        t = Expense.objects.all().filter(t_type=key,user= request.user)
        s = t.aggregate(Sum('amt'))['amt__sum']
        if s!= None:
            exp_dict[key] = s
        else:
            exp_dict[key] = 0
    for key in inc_type:
        t = Income.objects.all().filter(t_type=key,user= request.user)
        s = t.aggregate(Sum('amt'))['amt__sum']
        if s != None:
            inc_dict[key] = s
        else:
            inc_dict[key] = 0    
  
    inc_dict = dumps(inc_dict)
    exp_dict = dumps(exp_dict)
    
    return render(request, 'capstone/index.html',{'inc':inc_dict,'exp':exp_dict})





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
    if request.method == 'POST':
        rec_type = request.POST['rec_type']
        summary = request.POST['summary']
        t_type = request.POST['t_type']
        amt = request.POST['amt']
        
        
        if rec_type == 'Income':
            
            rec = Income.objects.create(user=request.user, summary=summary, t_type=t_type, amt=amt)
            rec.save()
        elif rec_type == 'Expense':
            
            rec = Expense.objects.create(user=request.user, summary=summary, t_type=t_type, amt=amt)
            rec.save()
    return render(request,"capstone/newentry.html")