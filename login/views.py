from django.shortcuts import render

from django import http
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils.functional import empty
from . models import profile
from django.contrib import auth
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model
#from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

#User = get_user_model() 
dbtable=profile.objects.all()
# Create your views here.
# def login(request):
#     if request.method=="POST":
        
#         email=request.POST["email"]
#         password=request.POST["password"]
#         for userdata in dbtable:
#             if userdata.email==email and userdata.password==password:
#                 return render(request,'home.html',{'userdata':userdata})

#         return redirect('/')
#     else:
#         return render(request,'login.html')

def login_page(request):
    
    if request.user.is_authenticated:
        return redirect('login') #change
    if request.method=="POST":
        
        username=request.POST["username"]
        password=request.POST["password"]
        dbtable=profile.objects.all()
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            userdata=profile.objects.get(name=username)
            if userdata.status:
                auth.login(request,user)
                print(user.get_username())
                #return redirect('home')
            else:
                messages.info(request,"You are blocked by admin")
                return redirect('/')

        else:
            messages.info(request,"Incorrect username or password")
            return redirect('/')
    return render(request,'login.html')
@login_required(login_url='login')
 
def signup(request):
    if request.method=='POST':
        userdata=profile()
        userdata.name=request.POST['username']
        userdata.email=request.POST['email']
        userdata.password=request.POST['password']
        cpassword=request.POST['cpassword']
        userdata.userdetails=request.POST['userdetails']
        #userdata.img=request.FILES['img']
        if(profile.objects.filter(name=userdata.name).exists() or User.objects.filter(username=userdata.name).exists()):
            messages.info(request,"An Error Occurred: Username is taken")
            print("Username is taken")
            return redirect('signup')
        elif(profile.objects.filter(email=userdata.email).exists() or User.objects.filter(username=userdata.name).exists()):
            messages.info(request,"An Error Occurred: Email ID is taken")
            print("Email ID is taken")
            return redirect('signup')
        
        if(cpassword == userdata.password):
            userdata.status=True
            userdata.save()
            user=User.objects.create_user(username=userdata.name,password=userdata.password,email=userdata.email,is_active=True,is_staff=False)
            user.save()
            auth.login(request,user)
            
            print("user created")
            return redirect('home')
        else:
            messages.info(request,"An Error Occurred: Password not matching")
            print("Password not matching")
            return redirect('signup')
    else:
        return render(request,'signup.html')
def logout(request):
    auth.logout(request)
    print("logout")
    return redirect('login')
    
# Create your views here.
