import base64
import os
import shutil

import requests
import transliterate
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from Blog.Form import FilmForm, NewStyleForm, RatingForm, FiltersForm, ResetForm, RecentForm, local_ResetForm
from Blog.models import Post, Rating, Actors, Prod, Styles
from authServer.models import Recent_res
from authServer.views import Logout
from extras import logger_mini
from extras.replacer import replacer
from extras.smpt_mail import send_mail


class Recent_Password_local(View):
    error = True
    form = local_ResetForm

    def get(self, request, request_token):
        if request.Auth_user:
            return render(request, 'blog/resetPassword.html', {'error': self.error})
        user = Recent_res.objects.filter(request_token=request_token).first().user
        return render(request, 'blog/resetPassword.html',
                      {'form': self.form(), 'method_who': 'New_password', 'who': 'Reset password',
                       'user': user.username})

    def post(self, request, request_token):
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, 'blog/resetPassword.html', {'error': self.error})
        returned = form.cleaned_data
        user = Recent_res.objects.filter(request_token=request_token).first()
        if user is not None:
            user.user.set_password(returned['name'])
            user.delete()
            return redirect('/login')
        return render(request, 'blog/resetPassword.html', {'error': self.error})


class Reset_Password(View):
    error = True
    form = ResetForm

    def get(self, request):
        if not request.Auth_user:
            return render(request, 'blog/resetPassword.html', {'error': self.error})
        return render(request, 'blog/resetPassword.html',
                      {'form': self.form(), 'method_who': 'Old_password', 'who': 'Reset password'})

    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, 'blog/resetPassword.html', {'error': self.error})
        returned = form.cleaned_data
        user = request.Auth_user
        if user.check_password(returned['name']):
            user.set_password(returned['new_name']).save()
            Logout().get(request)
            return redirect('/login')
        return render(request, 'blog/resetPassword.html', {'error': self.error})


class Recent_Password(View):
    error = True
    form = RecentForm

    def get(self, request):
        if request.Auth_user:
            return render(request, 'blog/resetPassword.html', {'error': self.error})
        return render(request, 'blog/resetPassword.html',
                      {'form': self.form(), 'method_who': 'Email', 'who': 'Recent password'})

    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, 'blog/resetPassword.html', {'error': self.error})
        returned = form.cleaned_data
        if not User.objects.filter(email=returned['emails']).exists():
            return render(request, 'blog/resetPassword.html', {'error': self.error})
        send_mail(os.getenv('email_login'), os.getenv('email_password'), returned['emails'])
        return redirect('/')


class New_Style(View):
    admin = False
    form = NewStyleForm
    error = True
    type = 'style'

    def get(self, request):
        if not request.Is_Anypermissions:
            return render(request, 'blog/new_prod.html', {'error': self.error})
        return render(request, 'blog/new_prod.html', {'admin': self.admin, 'form': self.form(), 'type': self.type})

    def post(self, request):
        form = self.form(request.POST)
        if not form.is_valid():
            return render(request, 'blog/new_prod.html', {'admin': self.admin, 'form': form, 'type': self.type})
        returned = form.cleaned_data
        if Styles.objects.filter(style=returned['Name']).exists():
            return render(request, 'blog/new_prod.html',
                          {'form': form, 'loggined': True, 'admin': True, 'type': 'style'})
        Styles.objects.create(style=returned['Name'])
        logger_mini.logger(request.Auth_user, 'ADD STYLE', f'{returned["Name"]}')
        return render(request, 'blog/new_prod.html', {'admin': self.admin, 'form': form, 'type': self.type})


class Moder_Panel(View):
    admin = True
    error = True

    def get(self, request):
        if not request.Is_Anypermissions:
            return render(request, 'blog/moderPanel.html', {'error': self.error})
        return render(request, 'blog/moderPanel.html', {'admin': self.admin})


class Admin_Panel(View):
    admin = True
    error = True

    def get(self, request):
        if not request.is_administrator:
            return render(request, 'blog/adminPanel.html', {'error': self.error})
        return render(request, 'blog/adminPanel.html', {'admin': self.admin})


class Filter(View):
    error, list_find = False, []

    def get(self, request):
        return render(request, 'blog/filters.html',
                      {'form': FiltersForm(), 'admin': request.Is_Anypermissions, 'error_local': self.error})

    def post(self, request):
        data_can = []
        form = FiltersForm(request.POST)
        if not form.is_valid():
            return redirect('/')
        form_data = form.cleaned_data
        if form_data['names'] != '':
            returned = Post.objects.filter(title__istartswith=form_data['names'])
            if returned.exists():
                data_can.append(returned.all())
        return render(request, 'blog/filters_list.html',
                      {'posts': data_can, 'admin': request.Is_Anypermissions})


class New_Film(View):
    int_for_actors, int_for_prods, form, admin = 0, 0, FilmForm(), False

    def get(self, request):
        if not request.Is_Anypermissions:
            return render(request, 'blog/new_film.html', {'error': True})
        return render(request, 'blog/new_film.html', {'form': self.form, 'admin': True})

    def post(self, request):
        form = FilmForm(request.POST)
        if not form.is_valid():
            return render(request, 'blog/new_film.html', {'error': True})
        returned = form.cleaned_data
        text_slug = replacer(transliterate.translit(returned['Title'], 'ru', reversed=True))
        if not request.POST.get('imgs_back'):
            link = f'https://imdb-api.com/API/SearchTitle/k_hfcfkmgb/{returned["Title"]}'
            photo_rest = requests.get(link).json()['results']
            if photo_rest:
                photo = photo_rest[0]['image']
                with open(f'authServer/static/photos/films/{text_slug}.png', 'wb+') as ava:
                    ava.write(requests.get(photo).content)
            else:
                shutil.copy('authServer/static/photos/films/standart_image.png',
                            f'authServer/static/photos/films/{text_slug}.png')
        else:
            with open(f'authServer/static/photos/films/{text_slug}.png', 'wb+') as ava:
                ava.write(base64.b64decode(request.POST.get('imgs_back').split('base64,')[1]))
        if Post.objects.filter(slug=text_slug):
            return render(request, 'blog/new_film.html', {'form': form, 'loggined': True})
        post_to_personal = Post.objects.create(title=returned['Title'], slug=text_slug, style=returned['style'],
                                               description=returned['description'], author=request.Auth_user)
        for one_in_actors in request.POST.getlist('kinput_name_2'):
            selected_actors = Actors.objects.get_or_create(name=one_in_actors)
            post_to_personal.actors.add(selected_actors)
        for one_in_producers in request.POST.getlist('kinput_name'):
            producers_returned, _created = Prod.objects.get_or_create(name=one_in_producers)
            post_to_personal.producer.add(producers_returned)
        logger_mini.logger(request.Auth_user, 'ADD FILM', f'{returned["Title"]}')
        return redirect('/')


class Post_List(View):
    def get(self, request):
        blog = []
        post_listin = Post.objects.all()
        text = Post.objects.order_by()[:3]
        for i in text:
            post_art = Post.objects.filter(title=i.title).first()
            post_rating = Rating.objects.filter(name=i).aggregate(all=Avg('stars'))
            blog.append(
                {'name': i.title, 'star': post_rating['all'], 'img': f'{post_art.slug}.png', 'slug': post_art.slug})
        return render(request, 'blog/list.html',
                      {'posts': post_listin, 'admin': request.Is_Anypermissions, 'the_best': blog})


class Post_Delete(View):
    def get(self, request, post):
        id_post = Post.objects.filter(slug=post)
        os.remove(f'authServer/static/photos/films/{id_post.first().slug}.png')
        if id_post.exists():
            id_post.first().delete()
        Rating.objects.filter(name=id_post.first()).delete()
        logger_mini.logger(request.Auth_user, 'REMOVE POST', f'{post}')
        return redirect('/')


class One_Post(View):
    form = RatingForm

    def get(self, request, post):
        form = True
        poster = get_object_or_404(Post, slug=post)
        if not Rating.objects.filter(username=request.Auth_user, name=poster).exists():
            form = self.form()
        rating_all = Rating.objects.filter(name=poster).aggregate(
            all=Avg('stars'),
            one=Count('stars', filter=Q(stars=1)),
            two=Count('stars', filter=Q(stars=2)),
            three=Count('stars', filter=Q(stars=3)),
            four=Count('stars', filter=Q(stars=4)),
            five=Count('stars', filter=Q(stars=5))
        )
        return render(request, 'blog/detail.html',
                      {'post': poster, 'actors': poster.actors.all(), 'producers': poster.producer.all(),
                       'admin': request.Is_Anypermissions, 'form': form, 'RatingAll': rating_all})

    def post(self, request, post):
        form = self.form(request.POST)
        poster = get_object_or_404(Post, slug=post)
        if not form.is_valid():
            return redirect(f'/{post}')
        stars = form.cleaned_data
        Rating.objects.create(name=poster, username=request.Auth_user, stars=stars['like'])
        return redirect(f'/{post}')
