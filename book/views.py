# coding=utf-8
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from book.models import *
# Create your views here.


def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'user' : user
    }
    return render(request, 'index.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy("index"))

    status = None
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse_lazy("index"))
        else:
            status = "error"
    content = {
        'user': None,
        'status': status
    }

    return render(request, "login.html", content)


def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy("index"))
    status = ""
    if request.method == "POST":
        password = request.POST.get('password', '')
        re_password = request.POST.get("re_password", '')
        if password != re_password or password == "":
            status = "re_error"
        else:
            username = request.POST.get("username", '')
            if User.objects.filter(username=username):
                status = "user existed"
            else:
                new_user = User.objects.create_user(username=username,password=password)
                new_user.save()
                new_my_user = MyUser(
                    user=new_user,
                    nickname=request.POST.get("nickname", ''),
                )
                new_my_user.save()
                status = "success"
    content = {
        'user':None,
        'status': status,
    }
    return render(request, "register.html", content)


@login_required(login_url=reverse_lazy('login'))
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse_lazy("index"))


# @login_required(login_url=reverse_lazy('login'))
def book_list(request):
    user = request.user if request.user.is_authenticated() else None
    if request.method == "POST":
        try:
            author = Author.objects.get(name=request.POST.get("author", ''))
        except:
            return HttpResponse('查无此作者')
        book_list = Book.objects.filter(author=author)
    else:
        book_list = Book.objects.all()
    content = {
        'book_list': book_list,
        'user': user
    }
    return render(request, 'list.html', content)


# @login_required(login_url=reverse_lazy("login"))
def detail(request, pk):
    user = request.user if request.user.is_authenticated() else None
    try:
        book = Book.objects.get(ISBN=pk)
    except:
        return HttpResponse("查无此书")
    content = {
        'user': user,
        'book': book,
    }
    return render(request, "detail.html", content)


@login_required(login_url=reverse_lazy("login"))
def delete(request, pk):
    try:
        book = Book.objects.get(ISBN=pk)
    except:
        return HttpResponse("查无此书")
    book.delete()
    return HttpResponseRedirect(reverse_lazy('list'))


@login_required(login_url=reverse_lazy("login"))
def add_book(request):
    user = request.user
    status = ""
    if request.method == "POST":
        if request.POST.get("ISBN", '') == "" or not request.POST.get('ISBN', '').isdigit():
            status = "ISBN error"
        else:
            new_book = Book(
                name=request.POST.get('name', ''),
                ISBN=request.POST.get('ISBN', ''),
                publisher=request.POST.get('publisher', ''),
                publish_date=request.POST.get("publish_date", ''),
                price=request.POST.get("price", ''),
                head_img=request.FILES.get('img', '')
            )
            new_book.save()
            if Author.objects.filter(name=request.POST.get('author', '')):
                new_book.author = Author.objects.filter(name=request.POST.get('author', ''))[0]
                new_book.save()
            else:
                new_author = Author(name=request.POST.get("author", ''))
                new_author.save()
                new_book.author = new_author
                new_book.save()
                return HttpResponseRedirect(reverse_lazy('addauthor') + '?name=%s' % request.POST.get('author', ''))
            status = "success"
    content = {
        'user': user,
        'status': status,
    }
    return render(request, "addbook.html", content)


@login_required(login_url=reverse_lazy("login"))
def add_author(request):
    user = request.user
    status = ""
    author_name = request.GET.get('name', '')
    author = Author.objects.get(name=author_name)
    if request.method == "POST":
        author.age = request.POST.get('age', '')
        author.country = request.POST.get('country', '')
        author.save()
        status = "success"
    content = {
        'author_name': author_name,
        'user': user,
        'status': status,
    }
    return render(request, 'addauthor.html', content)