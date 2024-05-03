from django.db import models
import re
from datetime import datetime

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if (len(postData['registered_first_name'])) == 0:
            errors['empty_first'] = "Please put in your first name."
        elif len(postData['registered_first_name']) < 2:
            errors['first_name_error'] = 'The first name has to be at least 2 characters.'

        if (len(postData['registered_last_name'])) == 0:
            errors['empty_last'] = "Please put in your last name."
        elif len(postData['registered_last_name']) < 2:
            errors['last_name_error'] = 'The last name has to be at least 2 characters.'

        if (len(postData['registered_email'])) == 0:
            errors['empty_email'] = "Please put in your email."
        elif not EMAIL_REGEX.match(postData['registered_email']):         
            errors['email'] = "Invalid email address!"

        if (len(postData['registered_password'])) == 0:
            errors['empty_pw'] = "Please put in your password."
        elif len(postData['registered_password']) < 8:
            errors['short_password'] = 'The password has to be at least 8 characters.'

        if postData['registered_password'] != postData['registered_confirm_pw']:
            errors['password_no_match'] = 'Your passwords do not match.'
        
        return errors

class TripManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['destination']) == 0:
            errors['empty_dest'] = "Please put in the destination."
        elif len(postData['destination']) < 3:
            errors['dest'] = "A trip destination must consist of at least 3 characters."
        
        if len(postData['start_date']) != 0:
            start_date = datetime.strptime(postData['start_date'], '%Y-%m-%d')
        if len(postData['start_date']) == 0:
            errors['empty_start'] = "Please choose the start date."
        elif start_date < datetime.today():
            errors['start'] = "Starting date must be in the future."
        
        if len(postData['end_date']) != 0:
            end_date = datetime.strptime(postData['end_date'], '%Y-%m-%d')
        if len(postData['end_date']) == 0:
            errors['empty_end'] = "Please choose the end date."
        elif len(postData['start_date']) != 0:
            if end_date < start_date:
                errors['end'] = "Time travel is not allowed at the trips. End date must be starting on/past the start date."
        elif len(postData['start_date']) == 0 and end_date < datetime.today():
            errors['end_early'] = "End date must be in the future."
        
        if len(postData['plan']) == 0:
            errors['empty_plan'] = "Please put in the plan details."
        elif len(postData['plan']) < 3:
            errors['plan'] = "A trip plan must consist of at least 3 characters."

        return errors

class Users(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    password = models.CharField(max_length=64)

    objects = UserManager()

class Trips(models.Model):
    destination = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.CharField(max_length=64)

    created_by = models.ForeignKey(
        Users,
        related_name='created_trips',
        on_delete=models.CASCADE
    )

    joined_by = models.ManyToManyField(
        Users,
        related_name='joined_trips'
    )

    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    objects = TripManager()