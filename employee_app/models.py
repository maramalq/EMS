from django.db import models
import re
import bcrypt
from datetime import datetime, date, timedelta

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters"
        today = datetime.today()
        date_from_form = datetime.strptime(postData['birthday'],'%Y-%m-%d')
        if date_from_form >= today:
            errors['birthday'] = "Birthday should be in the past"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email format!"
        user_list = User.objects.filter(email=postData['email'])
        if len(user_list) > 0:
            errors['not_unique'] = "Email is already exists"
        if len(postData['password']) < 8 :
            errors['password'] = "Password must be at least 8 characters"
        if postData['password'] != postData['conforin_pw']:
            errors['conforin_pw'] = "Conforim password does not mactch password"
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(postData['user_name']) == 0:
            errors['user_name'] = "Username is required"
        if len(postData['password']) < 8 :
            errors['password'] = "Password must be at least 8 characters"
        user_list = User.objects.filter(user_name=postData['user_name'])
        if len(user_list) == 0:
            errors['username2'] = "username not found!"
        elif not bcrypt.checkpw(postData['password'].encode(), user_list[0].password.encode()):
            errors['match'] = "Password not found in the database."
        return errors

    def edit_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name should be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):            
            errors['email'] = "Invalid email format!"
        return errors

class Department(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    birthday = models.DateField(default=datetime.now())
    position = models.BooleanField(default=False)
    total_salary = models.FloatField(default=0)
    email = models.CharField(max_length=255)
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    department =models.ForeignKey(Department, related_name="users",on_delete=models.CASCADE,null=True)

class AttandenceTable(models.Model):
    employee = models.ForeignKey(User, related_name="employee",on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now())
    attendence = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Attandence(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to="users/attandence")
    uploaded_at = models.DateTimeField(auto_now_add=True)