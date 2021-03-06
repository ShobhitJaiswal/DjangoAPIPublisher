# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
"""
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if (postData['first_name'].isalpha()) == False:
            if len(postData['first_name']) < 2:
                errors['first_name'] = "First name can not be shorter than 2 characters"

        if (postData['last_name'].isalpha()) == False:
            if len(postData['last_name']) < 2:
                errors['last_name'] = "Last name can not be shorter than 2 characters"

        if len(postData['email']) == 0:
            errors['email'] = "You must enter an email"

        if len(postData['password']) < 8:
            errors['password'] = "Password is too short!"

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    token = models.CharField(max_length=100, default="")
    objects = UserManager()
"""

class UserToken(AbstractUser):
    token=models.CharField(max_length=255,null=True,blank=True)

class PublisherManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if (postData['pname'].isalpha()) == False:
            if len(postData['pname']) < 2:
                errors['pname'] = "Name can not be shorter than 2 characters"

        if (postData['url'].isalpha()) == False:
            if len(postData['url']) < 2:
                errors['url'] = "URL can not be shorter than 2 characters"      
        
        return errors

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    objects = PublisherManager()

class APIManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if (postData['apis'].isalpha()) == False:
            if len(postData['apis']) < 1:
                errors['apis'] = "API name can not be shorter than 1 characters"

        if (postData['param[]'].isalpha()) == False:
            if len(postData['param[]']) < 2:
                errors['param[]'] = "API parameters can not be shorter than 2 characters"        
        
        return errors

class API(models.Model):
    name = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    api = models.CharField(max_length=25)
    api_parameters = models.CharField(max_length=255)
    objects = APIManager()
