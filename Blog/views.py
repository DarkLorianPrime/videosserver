import base64
import os
import shutil
import smtplib

import dotenv
import requests
import transliterate
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from Blog.Form import FilmForm, NewStyleForm, RatingForm, FiltersForm, ResetForm, RecentForm
from Blog.models import Post, Rating, Actors, Prod, Styles, Entire_rating
from authServer.views import Logout
from extras import logger_mini
from extras.replacer import replacer


class Reset_Password(View):
    error = True
    form = ResetForm

    def get(self, request):
        if not request.Auth_user:
            return render(request, 'blog/resetPassword.html', {'error': self.error})
        return render(request, 'blog/resetPassword.html', {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            user = request.Auth_user
            if user.check_password(returned['name']):
                user.set_password(returned['new_name'])
                user.save()
                Logout().get(request)
                return redirect('/login')
            else:
                return render(request, 'blog/resetPassword.html', {'error': self.error})


class Recent_Password(View):
    error = True
    form = RecentForm

    def get(self, request):
        if request.Auth_user:
            return render(request, 'blog/resetPassword.html', {'error': self.error})
        return render(request, 'blog/resetPassword.html', {'form': self.form()})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            returned = form.cleaned_data


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
        if form.is_valid():
            returned = form.cleaned_data
            if not Styles.objects.filter(style=returned['Name']).exists():
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
    actor, prod, error, list_find = False, False, False, []

    def get(self, request):
        return render(request, 'blog/filters.html',
                      {'form': FiltersForm(), 'admin': request.Is_Anypermissions, 'error_local': self.error})

    def post(self, request):
        form = FiltersForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if form_data['names'] != '':
                information = form_data['names'].split(',')
                for one_split in information:
                    returned = Post.objects.filter(title__startswith=form_data['names'])
                    if returned.exists():
                        return redirect(f'/{returned.first().slug}')
                    returned_actors = Post.objects.all().filter(producer=form_data['producer'], actors=form_data['actor'])
                    self.error = True
                    return render(request, 'blog/filters.html',
                                  {'form': form, 'admin': request.Is_Anypermissions, 'error_local': self.error})
            list_find = Post.objects.all().filter(producer=form_data['producer'], actors=form_data['actor'])
            return render(request, 'blog/list.html', {'posts': list_find, 'admin': request.Is_Anypermissions})


class New_Film(View):
    dictes_for_Actors, dictes_for_prods, int_for_actors, int_for_prods, form, admin = {}, {}, 0, 0, FilmForm(), False

    def get(self, request):
        if not request.Is_Anypermissions:
            return render(request, 'blog/new_film.html', {'error': True})
        return render(request, 'blog/new_film.html', {'form': self.form, 'admin': True})

    def post(self, request):
        form = FilmForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            text_for_slug = transliterate.translit(returned['Title'], 'ru', reversed=True, )
            text_slug = replacer(text_for_slug)
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
            Post_to_personal = Post.objects.create(title=returned['Title'], slug=text_slug, style=returned['style'],
                                                   description=returned['description'], author='darklorian')
            Entire_rating.objects.create(name=Post_to_personal, entire_stars=0.0)
            for one_in_actors in request.POST.getlist('kinput_name_2'):
                selected_actors = Actors.objects.create(name=one_in_actors)
                Post_to_personal.actors.add(selected_actors)
            for one_in_producers in request.POST.getlist('kinput_name'):
                selected_producer = Prod.objects.create(name=one_in_producers)
                Post_to_personal.producer.add(selected_producer)
            logger_mini.logger(request.Auth_user, 'ADD FILM', f'{returned["Title"]}')
            return redirect('/')
        return render(request, 'blog/new_film.html', {'form': self.form, 'admin': True})


class Post_List(View):
    @staticmethod
    def get(request):
        blog = []
        post_listin = Post.objects.all()
        text = Entire_rating.objects.order_by('-entire_stars')[:3]
        for i in text:
            post_art = Post.objects.filter(title=i.name).first()
            blog.append(
                {'name': str(i.name), 'star': i.entire_stars, 'img': f'{post_art.slug}.png', 'slug': post_art.slug})
        return render(request, 'blog/list.html',
                      {'posts': post_listin, 'admin': request.Is_Anypermissions, 'the_best': blog})


class Post_Delete(View):
    @staticmethod
    def get(request, post):
        id_post = Post.objects.filter(slug=post)
        os.remove(f'authServer/static/photos/films/{id_post.first().slug}.png')
        if id_post.exists():
            id_post.first().delete()
        entire = Entire_rating.objects.filter(name=id_post.first())
        if entire.exists():
            entire.first().delete()
        Rating.objects.filter(name=id_post.first()).delete()
        logger_mini.logger(request.Auth_user, 'REMOVE POST', f'{post}')
        return redirect('/')


class One_Post(View):
    form = RatingForm

    def get(self, request, post):
        integer_for_all_rating, dict_for_sum, form = 0, {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, 'all': 0}, True
        poster, user = get_object_or_404(Post, slug=post), request.Auth_user
        rating_all = Rating.objects.filter(name=poster)
        rating_for_this_post = Entire_rating.objects.filter(name=poster)
        one_in_actors_list, one_in_prods_list = [], []
        if rating_all.count() != 0:
            for rating in rating_all:
                dict_for_sum[str(rating.stars)] = dict_for_sum[str(rating.stars)] + 1
                integer_for_all_rating += int(rating.stars)
            dict_for_sum['all'] = integer_for_all_rating / rating_all.count()
        for dict_in_actors in poster.actors.all():
            one_in_actors_list.append(dict_in_actors.name)
        for dict_in_producers in poster.producer.all():
            one_in_prods_list.append(dict_in_producers.name)
        rating_for_this_post.update(entire_stars=dict_for_sum['all'])
        if not Rating.objects.filter(username=user, name=poster).exists():
            form = self.form()
        return render(request, 'blog/detail.html',
                      {'post': poster, 'actors': one_in_actors_list, 'prods': one_in_prods_list,
                       'admin': request.Is_Anypermissions, 'form': form, 'RatingAll': dict_for_sum})

    def post(self, request, post):
        form = self.form(request.POST)
        poster = get_object_or_404(Post, slug=post)
        if form.is_valid():
            stars = form.cleaned_data
            Rating.objects.create(name=poster, username=request.Auth_user, stars=stars['like'])
            return redirect(f'/{post}')
