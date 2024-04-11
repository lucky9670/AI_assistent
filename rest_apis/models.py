from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.
GENDER = (
    ("1", "Male"),
    ("2", "Female"),
    ("3", "Other"),
)

class User(AbstractUser):
    """
        Inherits from default User of Django and extends the fields.
        The following fields are part of Django User Model:
        | id
        | password
        | last_login
        | is_superuser
        | username
        | first_name
        | last_name
        | email
        | is_staff
        | is_active
        | date_joined
    """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    email = models.CharField(max_length=50, unique=True, null=False, blank=False)
    phone = models.CharField(max_length=13)
    gender =  models.CharField(max_length = 20, choices = GENDER, default = '1')
    age = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    image = models.ImageField(upload_to='profile', blank=True, null=True)
    prefrence = models.JSONField(null=True, blank=True)

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    trigger = models.JSONField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Reminder(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Activity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
