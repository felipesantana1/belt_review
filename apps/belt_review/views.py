from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

def index(request):
    return render(request, 'belt_review/index.html')

def books(request):
    last_three = Reviews.objects.all().order_by("-created_at")[:3]
    context = {
        'user': Users.objects.get(id=request.session['id']).alias,
        'books': Books.objects.all(),
        'reviews' : last_three
    }
    return render(request, 'belt_review/books.html', context)

def add(request):
    return render(request, 'belt_review/addBook.html')

def addBook(request):
    if len(request.POST['title']) < 2:
        messages.error(request, 'Book title must be at least 2 characters')
    if len(request.POST['author']) < 4:
        messages.error(request, 'Authors name must be at least 4 characters')
    if len(request.POST['review']) < 9:
        messages.error(request, 'Reveiew must contain at least 10 characters')
        return redirect('/books/add')
    else:
        author = Authors.objects.create(name=request.POST['author'])
        book = Books.objects.create(author=Authors.objects.get(id=author.id), title=request.POST['title'])
        Reviews.objects.create(user=Users.objects.get(id=request.session['id']), book=Books.objects.get(id=book.id), review=request.POST['review'], stars=int(request.POST['stars']))
    return redirect('/books/'+ str(book.id))

def addReview(request, id):
    if len(request.POST['review']) < 9:
        messages.error(request, 'Review must contain at least 10 characters')
        return redirect('/books/'+str(id))
    else:
        Reviews.objects.create(user=Users.objects.get(id=request.session['id']), book=Books.objects.get(id=id), review=request.POST['review'], stars=int(request.POST['stars']))
        return redirect('/books/'+str(id))

def display(request, id):
    context = {
        'book' : Books.objects.get(id=id),
        'reviews' : Reviews.objects.last()
    }
    return render(request, 'belt_review/displayBook.html', context)

def displayUser(request, id):
    context = {
        'user' : Users.objects.get(id=id),
        'reviews' : Reviews.objects.filter(user=Users.objects.get(id=id)).count()
    }
    return render(request, 'belt_review/displayUser.html', context)

def create(request):
    errors = Users.objects.regValidator(request.POST)
    if len(errors):
        for reg, error in errors.iteritems():
            messages.error(request, error, extra_tags=reg)
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = Users.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hashed_pw)
        request.session['id'] = user.id
        request.session['status'] = 'logged in'
    return redirect('/books')

def login(request):
    errors = Users.objects.logValidator(request.POST)
    if errors:
        for log, error in errors.iteritems():
            messages.error(request, error, extra_tags=log)
        return redirect('/')
    else:
        request.session['id'] = Users.objects.get(email=request.POST['email']).id
        request.session['status'] = 'logged in'
    return redirect('/books')

def logout(request):
    request.session.clear()
    return redirect('/')

def home(request):
    return redirect('/books')
