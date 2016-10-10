from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from models import User

def index(request):
    return render(request, 'loginApp/login.html')

def register(request):
    data = User.objects.isValidRegistration(request)
    if data[0] == False:
        print_messages(request, data[1])
        return redirect(reverse('users:index'))
    return log_user_in(request, data[1])

def login(request):
    data = User.objects.isValidLogin(request)
    if data[0] == False:
        print_messages(request, data[1])
        return redirect(reverse('users:index'))
    return log_user_in(request, data[1])

def log_user_in(request, user):
    request.session['user'] = {
        'id' : user.id,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'email' : user.email,
    }
    return redirect(reverse('users:success'))

def success(request):
    if not 'user' in request.session:
        return redirect(reverse('users:index'))
    return redirect(reverse('reviews:index'))

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.ERROR, message)

def logout(request):
    request.session.pop('user')
    return redirect(reverse('users:index'))
