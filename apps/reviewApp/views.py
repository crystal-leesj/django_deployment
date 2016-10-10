from django.shortcuts import render, redirect
from django.urls import reverse
from models import Author, Book, Review
from ..loginApp.models import User
from ..loginApp.views import print_messages


def check_logged_in(request):
    return 'user' in request.session

# GET Home
def index(request):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    context = {
        'reviews' : Review.objects.fetch_recent(),
        'books' : Book.objects.all()
    }
    return render(request, 'reviewApp/index.html', context)

# GET create new review
def new(request):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    context = {
        'books' : Book.objects.all(),
        'authors' : Author.objects.all()
    }
    return render(request, 'reviewApp/new.html', context)

# POST book review
def create(request):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    print "UserId::::::: ", request.session['user']['id']
    result = Review.objects.create_review(request.POST, request.session['user']['id'])

    if result[0] == True:
        return redirect(reverse('reviews:index', kwargs={'id': result[1].book.id }))
    else:
        print_messages(request, result[1])
        return redirect(reverse('reviews:new'))

# GET show book
def show(request, id):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    book = Book.objects.get(id=id)
    return render(request, 'reviewApp/show.html', { 'book' : book })


def show_user(request, id):
    if not check_logged_in(request):
        return redirect(reverse('users:index'))

    user = User.objects.fetch_user_info(id)
    return render(request, 'reviewApp/show_user.html', { 'user' : user })
