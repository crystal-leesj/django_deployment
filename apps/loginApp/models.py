from __future__ import unicode_literals
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Count
import bcrypt, re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')

class UserManager(models.Manager):
    def isValidRegistration(self, request):
        errors = []
        if len(request.POST['first_name']) < 2:
            errors.append('First Name can not be less than 2 characters')
        elif not request.POST['first_name'].isalpha():
            errors.append('First Name should only contain letters')

        if len(request.POST['last_name']) < 2:
            errors.append('Last Name can not be less than 2 characters')
        elif not request.POST['last_name'].isalpha():
            errors.append('Last Name should only contain letters')

        if len(request.POST['email']) < 1:
            errors.append('Email can not be empty')
        elif not EMAIL_REGEX.match(request.POST['email']):
            errors.append('Email is not valid')

        if len(request.POST['password']) < 1:
            errors.append('Password can not be empty')
        elif len(request.POST['password']) < 8:
            errors.append('Password should be more than 7 characters')
        elif not PASSWORD_REGEX.match(request.POST['password']):
            errors.append('Password should contain at least one upper case letter and one number')

        if request.POST['password'] != request.POST['confirm_password']:
            errors.append('Password and Confirm Password does not match!')

        try:
            user = User.objects.get(email = request.POST['email'])
            errors.append('This email is already being used')
        except ObjectDoesNotExist:
            pass

        if len(errors) > 0:
            return [False, errors]

        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = self.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        return [True, user]

    def isValidLogin(self, request):
        errors = []
        try:
            user = User.objects.get(email = request.POST['email'])
            password = user.password.encode()
            login_input_password = request.POST['password'].encode()
            print "*"*40
            print password
            print bcrypt.hashpw(login_input_password, password)
            print "*"*40
            if bcrypt.hashpw(login_input_password, password) == password:
                return (True, user)
            else:
                errors.append("Sorry, no password match")
                return (False, errors)
        except ObjectDoesNotExist:
            pass
        errors.append("Sorry, no email found. Please try again.")
        return (False, errors)



    def fetch_user_info(self, id):
        return self.filter(id=id).annotate(total_reviews=Count('review'))[0]




class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
