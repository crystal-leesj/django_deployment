from __future__ import unicode_literals
from ..loginApp.models import User
from django.db import models

class ReviewManager(models.Manager):
    def create_review(self, form_data, user_id):
        try:
            # author = self.fetch_author(form_data)
            book = self.fetch_book(form_data)
            # book = Book.objects.create(title=form_data['title'], author=author)
            user = User.objects.get(id=user_id)
            new_review = Review.objects.create(review=form_data['review'], rating=form_data['rating'], user=user, book=book)
            return (True, new_review)
        except:
            return (False, ["There was a problem creating the review..."])

    def fetch_book(self, form_data):
        try:
            book = Book.objects.get(id=form_data['book_id'])
        except:
            author = self.fetch_author(form_data)
            book = Book.objects.create(title=form_data['title'], author=author)
        return book

    def fetch_author(self, form_data):
        try:
            print 'author_id::::::::::', form_data['author_id']
            author = Author.objects.get(id=form_data['author_id'])
        except:
            print 'errorrrr'
            author = Author.objects.create(name=form_data['new_author'])
        return author

    def fetch_recent(self):
        return Review.objects.all().order_by('-created_at')[:3]



class Author(models.Model):
    name = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Book(models.Model):
    title = models.CharField(max_length=45)
    author = models.ForeignKey('Author')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Review(models.Model):
    review = models.TextField(max_length=1000)
    rating = models.IntegerField()
    user = models.ForeignKey('loginApp.User')
    book = models.ForeignKey('Book', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()
