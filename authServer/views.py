import uuid

from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect

from extras.check_person import get_login
from .models import cookie_saves, not_Admin, Admin, not_Moderator, Moderator
from .Form import LoginForm, RegistrationForm, new_adminForm, new_moderForm


def auth(request):
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
    else:
        if get_login(request)[0] is not False:
            return redirect('/')
        form = LoginForm()
    return render(request, 'blog/post/share.html', {'form': form, 'loggined': False})


def profile(request):
    text = get_login(request)
    if text[0] is False:
        return render(request, 'blog/get/profile.html', {'error': True})
    return render(request, 'blog/get/profile.html', {'user': text[0], 'ToFAdm': text[1], 'ToFModer': text[2]})


def registration(request):
    form = RegistrationForm()
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
        else:
            loggined = True
    else:
        if get_login(request)[0] is not False:
            return redirect('/')
        loggined = False
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
    if text[0] is False or text[1] is False:
        return render(request, 'blog/post/new_admin.html', {'error': True})
    loggined = True
    return render(request, 'blog/post/new_admin.html', {'form': form, 'loggined': loggined, 'new': 'moderator'})


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
    if text[0] is False or text[1] is False:
        return render(request, 'blog/post/new_admin.html', {'error': True})
    return render(request, 'blog/post/new_admin.html', {'form': form, 'loggined': True, 'new': 'administrator'})


def logout(request):
    d = cookie_saves.objects.filter().first()
    if d is not None:
        d.delete()
        req = redirect('/login/')
        req.delete_cookie('loggined_token')
        return req
