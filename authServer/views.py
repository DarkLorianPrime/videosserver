from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from extras.authentication import BackendAuth
from .Form import RegistrationForm, LoginForm, new_moderForm, new_adminForm, AdminDeleteForm, ModerDeleteForm
from .models import cookie_saves, Admin, Moderator, Role


# from .Form import LoginForm, RegistrationForm, new_adminForm, new_moderForm, DelUserForm, ModerDeleteForm, \
#     AdminDeleteForm


def del_user(request):
    form, text = DelUserForm(), get_login(request)
    if request.is_moderator:
        return render(request, 'blog/post/deluser.html', {'error': True})
    if request.method == 'POST':
        form = DelUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(username=cd['name']).first()
            if user is not None:
                user.delete()
                # not_Moderator.objects.filter(name=cd['name']).first().delete()
                # not_admin = not_Admin.objects.filter(name=cd['name']).first()
                # if not_admin is not None:
                #     not_admin.delete()
    return render(request, 'blog/post/deluser.html', {'form': form, 'who': 'user'})


def del_moderator(request):
    form = ModerDeleteForm()  # Need fix!
    if not request.is_administrator:
        return render(request, 'blog/post/deluser.html', {'error': True})
    if request.method == 'POST':
        form = ModerDeleteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            find = Moderator.objects.filter(name=cd['name']).first()
            if find is not None:
                find.delete()
                # not_Moderator.objects.create(name=cd['name'])
    return render(request, 'blog/post/deluser.html', {'form': form, 'who': 'moderator'})


def del_administrator(request):
    form = AdminDeleteForm()  # Need fix!
    if not request.is_administrator:
        return render(request, 'blog/post/deluser.html', {'error': True})
    if request.method == 'POST':
        form = AdminDeleteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            find = Admin.objects.filter(name=cd['name']).first()
            if find is not None:
                find.delete()
    return render(request, 'blog/post/deluser.html', {'form': form, 'who': 'administrator'})


def auth(request):
    if request.Auth_user is not None:
        return redirect('/')
    form, trouble = LoginForm(), False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Login_return = BackendAuth().authenticate(request=request, username=cd['login'], password=cd['password'])
            if not Login_return.get('error'):
                return Login_return
            trouble = True
    return render(request, 'blog/post/share.html', {'form': form, 'trouble': trouble})


def profile(request):
    administrator = BackendAuth().is_Administrator(request)
    moderator = BackendAuth().is_Moderator(request)
    return render(request, 'blog/get/profile.html', {'ToFAdm': administrator, 'ToFModer': moderator, 'error': False})


def registration(request):
    form, trouble = RegistrationForm(), False
    if request.Auth_user is not None:
        return redirect('/')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            Registration_return = BackendAuth().authenticate(request=request, username=returned['login'],
                                                             password=returned['password'],
                                                             email=returned['email'], registration=True)
            if Registration_return.get('error') == 'username':
                trouble = 'Login'
            elif Registration_return.get('error') == 'email':
                trouble = 'Email'
            else:
                return Registration_return
    return render(request, 'blog/post/registration.html', {'form': form, 'trouble': trouble, 'error': False})


def add_moderator(request):
    form = new_moderForm()
    if request.method == 'POST':
        form = new_moderForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            Moderator.objects.create(name=returned['nick'])
    if not request.is_administrator:
        return render(request, 'blog/post/new_admin.html', {'error': True})
    return render(request, 'blog/post/new_admin.html', {'form': form, 'loggined': True, 'new': 'moderator'})


def add_admin(request):
    if not BackendAuth().is_Administrator(request):
        return render(request, 'blog/post/new_admin.html', {'error': True})
    form = new_adminForm()
    if request.method == 'POST':
        form = new_adminForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            User_Model = User.objects.filter(username=returned['nick'])
            Role_selected = Role.objects.filter(name='Administrator', Users=User_Model)
            Role_selected_Mod = Role.objects.filter(name='Moderator', Users=User_Model)
            if not Role_selected.is_Role:
                Role_selected.is_Role = True
                Role_selected.save()
            if not Role_selected_Mod.is_Role:
                Role_selected_Mod.is_Role = True
                Role_selected_Mod.save()
    return render(request, 'blog/post/new_admin.html', {'form': form, 'loggined': True, 'new': 'administrator'})


def logout(request):
    d = cookie_saves.objects.filter().first()
    if d is not None:
        d.delete()
        req = redirect('/login/')
        req.delete_cookie('loggined_token')
        return req
    return redirect('/')
