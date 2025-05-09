from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from application.models import user, sessions, skills, user_skills
from django.contrib import messages


# Create your views here.
def home(req):
    return render(req, 'html/homepage.html')

def main(req):
    mentors = user.objects.filter(is_mentor=True)
    for mentor in mentors:
        print(mentor.is_mentor)
    print('mentors ',mentors)
    return render(req, 'html/MainPage.html',{'mentors':mentors})

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
            is_mentor=req.POST['is_mentor'],
        )
        print('user1',user1)
        user1=user.objects.get(username=req.POST['username'])
        logout(req)
        if user1:
            messages.success(req, 'User created successfully')
            login(user=user1,request=req)
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

def mentorPage(req, username):
    print('id', id)
    mentor = user.objects.get(username=username)
    sessions_vals = sessions.objects.filter(mentor_id=mentor)
    print('mentor', mentor)
    return render(req, 'html/MentorPage.html', {'mentor': mentor,'sessions': sessions_vals})