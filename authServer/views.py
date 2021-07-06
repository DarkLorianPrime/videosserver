from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from extras import logger_mini
from extras.Delete_users_role import deleter
from extras.authentication import BackendAuth
from .Form import RegistrationForm, LoginForm, new_moderForm, new_adminForm, AdminDeleteForm, ModerDeleteForm, \
    DelUserForm
from .models import cookie_saves, Role
from Blog.models import Rating


class Delete_User(View):
    form = DelUserForm

    def get(self, request):
        if not request.Is_Anypermissions:
            return render(request, 'blog/deluser.html', {'error': True})
        return render(request, 'blog/deluser.html', {'form': self.form(), 'who': 'user'})

    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, 'blog/deluser.html', {'error': True})
        form_data = form.cleaned_data
        user = User.objects.filter(username=form_data['name']).first()
        if user is not None:
            user.delete()
        return render(request, 'blog/deluser.html', {'form': form, 'who': 'user'})


class Delete_Moderators(View):
    form = ModerDeleteForm

    def get(self, request):
        if not request.is_administrator:
            return render(request, 'blog/deluser.html', {'error': True})
        return render(request, 'blog/deluser.html', {'form': self.form(), 'who': 'moderator'})

    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, 'blog/deluser.html', {'error': True})
        form_data = form.cleaned_data
        deleter(form_data, request, 4, 2)
        return render(request, 'blog/deluser.html', {'form': form, 'who': 'moderator'})


class Delete_Administrator(View):
    form = AdminDeleteForm

    def get(self, request):
        if not request.is_administrator:
            return render(request, 'blog/deluser.html', {'error': True})
        return render(request, 'blog/deluser.html', {'form': self.form(), 'who': 'administrator'})

    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, 'blog/deluser.html', {'error': True})
        form_data = form.cleaned_data
        deleter(form_data, request, 3, 4)
        return render(request, 'blog/deluser.html', {'form': form, 'who': 'administrator'})


class Auth(View):
    trouble = False
    form = LoginForm

    def get(self, request):
        return render(request, 'blog/share.html', {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, 'blog/share.html', {'error': True})
        form_data = form.cleaned_data
        Login_return = BackendAuth().authenticate(request=request, username=form_data['login'],
                                                  password=form_data['password'])
        if not Login_return.get('error'):
            return Login_return
        return render(request, 'blog/share.html', {'form': self.form, 'trouble': Login_return['error']})


class Profile(View):
    error = False

    def get(self, request):
        r = Rating.objects.filter(username=request.Auth_user).order_by('-stars').first()
        return render(request, 'blog/profile.html',
                      {'ToFAdm': request.is_administrator, 'ToFModer': request.Is_Anypermissions, 'error': self.error,
                       'fav_film': r.name if r is not None else None})


class Registration(View):
    form = RegistrationForm

    def get(self, request):
        return render(request, 'blog/registration.html', {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, 'blog/registration.html', {'error': True})
        form_data = form.cleaned_data
        Registration_return = BackendAuth().authenticate(request=request, username=form_data['login'],
                                                         password=form_data['password'],
                                                         email=form_data['email'], registration=True)
        if Registration_return.get('error'):
            trouble = Registration_return.get('error')
        else:
            return Registration_return
        return render(request, 'blog/registration.html',
                      {'form': self.form(), 'trouble': trouble, 'error': False})


class Add_Moderator(View):
    form = new_moderForm

    def get(self, request):
        if not request.is_administrator:
            return render(request, 'blog/new_admin.html', {'error': True})
        return render(request, 'blog/new_admin.html', {'form': self.form(), 'loggined': True, 'new': 'moderator'})

    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, 'blog/new_admin.html', {'error': True})
        form_data = form.cleaned_data
        deleter(form_data, request, 2, 4)
        return render(request, 'blog/new_admin.html', {'form': form, 'loggined': True, 'new': 'moderator'})


class Add_Admin(View):
    form = new_adminForm

    def get(self, request):
        if not request.is_administrator:
            return render(request, 'blog/new_admin.html', {'error': True})
        return render(request, 'blog/new_admin.html', {'form': self.form(), 'loggined': True, 'new': 'administrator'})

    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, 'blog/new_admin.html', {'error': True})
        form_data = form.cleaned_data
        deleter(form_data, request, 4, 3)
        return render(request, 'blog/new_admin.html', {'form': form, 'loggined': True, 'new': 'administrator'})


class Logout(View):

    def get(self, request):
        form_data = redirect('/login/')
        cookie_saves.objects.filter(cookie_user_data=request.Auth_user).delete()
        form_data.delete_cookie('loggined_token')
        return form_data
