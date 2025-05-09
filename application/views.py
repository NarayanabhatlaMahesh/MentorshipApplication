from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from application.models import user, sessions, skills, user_skills
from django.contrib import messages


# Create your views here.
def home(req):
    return render(req, 'html/homepage.html')

def main(req):
    return render(req, 'html/MainPage.html')

def register(req):
    if req.method=='POST':
        print('post',req.POST)
        user1 = user.objects.get_or_create(
            username=req.POST['username'],
            email=req.POST['email'],
            password=req.POST['password'],
            first_name=req.POST['first_name'],
            last_name=req.POST['last_name'],
            phone_number=req.POST['phone_number'],
            city=req.POST['city'],
            state=req.POST['state'],
            country=req.POST['country'],
            zip_code=req.POST['zip_code'],
        )
        print('user1',user1)
        if user1:
            messages.success(req, 'User created successfully')
            return redirect('main')
        else:
            return render(req, 'Register.html', {'error': 'User already exists'})
    return render(req, 'Register.html')

def Login(req):
    if req.method=='POST':
        print('post',req.POST)
        user1 = user.objects.get(
            username=req.POST['username'],
            password=req.POST['password'],
        )
        print('user1',user1)
        if(user1):
            login(user=user1, request=req)
            return redirect('main')
        else:
            return render(req, 'Register.html', {'error': 'User already exists'})
    return render(req, 'html/Login.html')
def Logout(req):
    logout(req)
    return redirect('home')