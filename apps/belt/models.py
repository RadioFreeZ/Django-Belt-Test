from __future__ import unicode_literals
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import datetime
from datetime import timedelta
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "Name must have 2 or more characters!"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Name must have 2 or more characters!"
        if len(postData['email']) < 1:
            errors["email"] = "Email cannot be blank!"
        email_check = User.objects.filter(email = postData['email'])
        if email_check:
            errors["email"] = "Email already in use!"
        if len(postData['password']) < 8:
            errors["password"] = "Password must have 8 or more characters!"
        try:
            validate_email(postData['email'])
            valid_email = True
        except ValidationError:
            valid_email = False
            errors["email"] = "Email not in correct format!"
        date_time = datetime.datetime.now() - timedelta(days=365*18)
        date_time = f'{date_time:%Y-%m-%d}'
        print(type(date_time))
        print(type(postData['birthday']))
        if postData['birthday'] > date_time:
            errors["birthday"] = "Invalid birthday!"
        return errors

class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3:
            errors["title"] = "Title must have 3 or more characters!"
        if len(postData['description']) < 3:
            errors["description"] = "Description must have 3 or more characters!"
        if len(postData['location']) < 3:
            errors["location"] = "Location cannot be blank!"
        try:
            if len(postData['cat1']) < 1 and len(postData['cat2']) < 1:
                errors["cat"] = "Job must have a category!"
        except:
            try:
                if len(postData['cat2']) < 1:
                    errors["cat"] = "Job must have a category!"
            except:
                pass
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    birthday = models.DateField(auto_now=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=255, default = "")
    poster = models.ForeignKey(User,related_name = "posted_jobs")
    worker = models.ForeignKey(User,related_name = "worked_jobs", default = "")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobManager()
