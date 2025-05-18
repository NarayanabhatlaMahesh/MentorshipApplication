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
    mentor = models.ManyToManyField(user, related_name='mentor_session')
    session_date = models.DateTimeField(auto_now_add=True)
    session_time = models.TimeField()
    mentee = models.ManyToManyField(user, related_name='mentee_session')
    is_completed = models.BooleanField(default=False)
    

class skills(models.Model):
    skill = models.CharField(max_length=100)
    skill_id = models.AutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.skill

class user_skills(models.Model):
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    skill_id = models.ForeignKey(skills, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.user_id.username} - {self.skill_id.skill}"

class mentorSlots(models.Model):
    mentor = models.ForeignKey(user, on_delete=models.CASCADE)
    from_time = models.TimeField()
    to_time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.mentor.username} - {self.from_time} - {self.to_time}"
    
# class sessions(models.Model):
#     session_id = models.AutoField(primary_key=True)
#     mentor = models.ManyToManyField(user, related_name='mentor_session')
#     mentor_slot = models.ForeignKey(mentorSlots, on_delete=models.CASCADE)
#     mentee = models.ManyToManyField(user, related_name='mentee_session')
#     is_completed = models.BooleanField(default=False)

class slots(models.Model):
    slot_id = models.AutoField(primary_key=True)
    from_time = models.TextField()
    to_time = models.TextField()
    
    def __str__(self):
        return f"{self.from_time} - {self.to_time}"

class notifications(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"