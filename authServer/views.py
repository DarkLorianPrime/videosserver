import uuid

from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

from extras.check_person import get_login
from .models import cookie_saves, not_Admin, Admin, not_Moderator, Moderator
from .Form import LoginForm, RegistrationForm, new_adminForm, new_moderForm, DelUserForm, ModerDeleteForm, \
    AdminDeleteForm


def del_user(request):
    form, text = DelUserForm(), get_login(request)
    if text[2] is False:
        return render(request, 'blog/post/deluser.html', {'error': True})
    if request.method == 'POST':
        form = DelUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(username=cd['name']).first()
            if user is not None:
                user.delete()
                not_Moderator.objects.filter(name=cd['name']).first().delete()
                not_admin = not_Admin.objects.filter(name=cd['name']).first()
                if not_admin is not None:
                    not_admin.delete()
    return render(request, 'blog/post/deluser.html', {'form': form, 'who': 'user'})


def del_moderator(request):
    form, text = ModerDeleteForm(), get_login(request)
    if text[1] is False:
        return render(request, 'blog/post/deluser.html', {'error': True})
    if request.method == 'POST':
        form = ModerDeleteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            find = Moderator.objects.filter(name=cd['name']).first()
            if find is not None:
                find.delete()
                not_Moderator(name=cd['name']).save()
    return render(request, 'blog/post/deluser.html', {'form': form, 'who': 'moderator'})


def del_administrator(request):
    form, text = AdminDeleteForm(), get_login(request)
    if text[1] is False:
        return render(request, 'blog/post/deluser.html', {'error': True})
    if request.method == 'POST':
        form = AdminDeleteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            find = Admin.objects.filter(name=cd['name']).first()
            if find is not None:
                find.delete()
                not_Admin(name=cd['name']).save()
    return render(request, 'blog/post/deluser.html', {'form': form, 'who': 'administrator'})


def auth(request):
    form = LoginForm()
    if get_login(request)[0] is not False:
        return redirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            obj = User.objects.filter(username=cd['login']).first()
            if obj is None:
                return render(request, 'blog/post/share.html', {'form': form, 'loggined': True})
            if obj.check_password(raw_password=cd['password']) is not True:
                return render(request, 'blog/post/share.html', {'form': form, 'loggined': True})
            data = uuid.uuid4().hex
            red = redirect('/')
            if cookie_saves.objects.filter(cookie_user_id=obj.id).first() is None:
                cookie_saves(cookie_user_id=obj.id, cookie_user_token=data).save()
                red.set_cookie(key='loggined_token', value=data, max_age=100000)
            return red
    return render(request, 'blog/post/share.html', {'form': form, 'loggined': False})


def profile(request):
    text = get_login(request)
    if text[0] is False:
        return render(request, 'blog/get/profile.html', {'error': True})
    return render(request, 'blog/get/profile.html', {'user': text[0], 'ToFAdm': text[1], 'ToFModer': text[2]})


def registration(request):
    form, loggined = RegistrationForm(), False
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if User.objects.filter(username=cd['login']).first() is not None:
                return render(request, 'blog/post/registration.html', {'form': form, 'loggined': 'Login'})
            if User.objects.filter(email=cd['email']).first() is not None:
                return render(request, 'blog/post/registration.html', {'form': form, 'loggined': 'Email'})
            User.objects.create_user(username=cd['login'], password=cd['password'], email=cd['email']).save()
            data, red, obj = uuid.uuid4().hex, redirect('/'), User.objects.filter(username=cd['login']).first()
            cookie_saves(cookie_user_id=obj.id, cookie_user_token=data).save()
            not_Admin(name=cd['login']).save()
            not_Moderator(name=cd['login']).save()
            red.set_cookie(key='loggined_token', value=data, max_age=100000)
            return red
        loggined = True
    if get_login(request)[0] is not False:
        return redirect('/')
    return render(request, 'blog/post/registration.html', {'form': form, 'loggined': loggined})


def add_moderator(request):
    form = new_moderForm()
    if request.method == 'POST':
        form = new_moderForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            not_Moderator.objects.get(name=returned['nick']).delete()
            Moderator(name=returned['nick']).save()
    text = get_login(request)
    if text[1] is False:
        return render(request, 'blog/post/new_admin.html', {'error': True})
    return render(request, 'blog/post/new_admin.html', {'form': form, 'loggined': True, 'new': 'moderator'})


def add_admin(request):
    form = new_adminForm()
    if request.method == 'POST':
        form = new_adminForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            not_Admin.objects.get(name=returned['nick']).delete()
            Admin(name=returned['nick']).save()
            not_Moderator.objects.get(name=returned['nick']).delete()
            Moderator(name=returned['nick']).save()
    text = get_login(request)
    if text[1] is False:
        return render(request, 'blog/post/new_admin.html', {'error': True})
    return render(request, 'blog/post/new_admin.html', {'form': form, 'loggined': True, 'new': 'administrator'})


def logout(request):
    d = cookie_saves.objects.filter().first()
    if d is not None:
        d.delete()
        req = redirect('/login/')
        req.delete_cookie('loggined_token')
        return req
