from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class user(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_mentor = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

class sessions(models.Model):
    session_id = models.AutoField(primary_key=True)
    mentor_id = models.ForeignKey(user, on_delete=models.CASCADE, related_name='mentor')
    session_date = models.DateTimeField(auto_now_add=True)
    session_time = models.TimeField()
    mentee_id = models.ForeignKey(user, on_delete=models.CASCADE, related_name='mentee')
    is_completed = models.BooleanField(default=False)
    def __str__(self):
        return f"Session {self.session_id} - Mentor: {self.mentor_id.username} - Mentee: {self.mentee_id.username}"

class skills(models.Model):
    skill = models.CharField(max_length=100)
    skill_id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.skill

class user_skills(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(skills, on_delete=models.CASCADE)
    proficiency_level = models.CharField(max_length=100)
    years_of_experience = models.IntegerField()
    def __str__(self):
        return f"{self.user_id.username} - {self.skill_id.skill} - {self.proficiency_level}"
