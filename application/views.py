from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from application.models import user, sessions, skills, user_skills
from django.contrib import messages
from datetime import datetime

# Create your views here.
def home(req):
    return render(req, 'html/homepage.html')

def main(req):
    mentors = user.objects.filter(is_mentor=True)
    for mentor in mentors:
        print(mentor.is_mentor)
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
        user1 = user.objects.get(
            username=req.POST['username'],
            password=req.POST['password'],
        )
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
    if req.method=='GET':
        try:
            mentor = user.objects.get(username=username)
            print('mentor asked is ',mentor)
            print([i.skill_id.skill for i in user_skills.objects.filter(user_id=mentor)])
            mentors_skills=list(set([skills.objects.get(skill_id=i.skill_id.skill_id) for i in user_skills.objects.filter(user_id=mentor)]))
            print('mentors skills are ',mentors_skills)
        except user.DoesNotExist:
            messages.error(req, 'Mentor not found')
            return redirect('main')
        return render(req, 'html/MentorPage.html', {'mentor': mentor,'mentor_skills': mentors_skills})  
    if req.method=='POST':
        print('uesrname in mentorpage is ',username)
        mentor = user.objects.filter(username=username)[0]
        print('mentor values ',vars(mentor))
        sess = sessions.objects.create(session_time=datetime.now(),session_date=req.POST['session_date'])
        sess.save()
        print(sess.mentor)
        sess.mentor.add(mentor)
        sess.mentee.add(req.user)
        sess.save()
        print([m.username for m in sess.mentor.all()])
        messages.success(req, 'Session created successfully')
        return redirect('main')
    

def skillsPage(req):
    if req.method=='POST':
        for skill in req.POST['skill_name']:
            user_skills.objects.create(
                user_id=req.user,
                skill_id=skills.objects.get(skill=skill),
                proficiency_level=req.POST['proficiency_level'],
                years_of_experience=req.POST['years_of_experience'],
            )
        skill = user_skills.objects.get_or_create(
            skill_name=req.POST['skill_name'],
            skill_description=req.POST['skill_description'],
        )
        if skill:
            messages.success(req, 'Skill created successfully')
            return redirect('skillsPage')
        else:
            return render(req, 'html/Skills.html', {'error': 'Skill already exists'})
    return render(req, 'html/Skills.html')

def profilePage(req):
    skills_List = skills.objects.all()
    user_skills_list = [skills.objects.get(skill_id=i['skill_id_id']) for i in user_skills.objects.filter(user_id=req.user).values()]
    if req.method=='POST':
        for i in req.POST.getlist('skills'):
            user_skills.objects.create(user_id = req.user,skill_id=skills.objects.get(skill_id=int(i))).save()
    return render(req, 'html/ProfilePage.html',{'skills':skills_List,'user_skills':user_skills_list})