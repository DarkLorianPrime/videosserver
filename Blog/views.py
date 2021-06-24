import base64
import shutil

import requests
import transliterate
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from Blog.Form import FilmForm, NewStyleForm, RatingForm, FiltersForm
from Blog.models import Post, Rating, Actors, Prod, Styles, Entire_rating
from extras import logger_mini
from extras.replacer import replacer


class New_Style(View):
    admin = False
    form = NewStyleForm
    error = True
    who = 'style'

    def get(self, request):
        if not request.Is_Anypermissions:
            return render(request, 'blog/new_prod.html', {'error': self.error})
        return render(request, 'blog/new_prod.html', {'admin': self.admin, 'form': self.form(), 'who': self.who})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            if Styles.objects.filter(style=returned['Name']).first() is not None:
                return render(request, 'blog/new_prod.html',
                              {'form': form, 'loggined': True, 'admin': True, 'who': 'style'})
            Styles.objects.create(style=returned['Name'])
            logger_mini.logger(request.Auth_user, 'ADD STYLE', f'{returned["Name"]}')
        return render(request, 'blog/new_prod.html', {'admin': self.admin, 'form': form, 'who': self.who})


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
    actor, prod, er_l, list_find = False, False, False, []

    def get(self, request):
        return render(request, 'blog/filters.html',
                      {'form': FiltersForm(), 'admin': request.Is_Anypermissions, 'error_local': self.er_l})

    def post(self, request):
        form = FiltersForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if form_data['names'] != '':
                returned = Post.objects.filter(title__startswith=form_data['names']).first()
                if returned is not None:
                    return redirect(f'/{returned.slug}')
                else:
                    self.er_l = True
                return render(request, 'blog/filters.html',
                              {'form': form, 'admin': request.Is_Anypermissions, 'error_local': self.er_l})
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
                    message = request.POST.get('imgs_back')
                    ava.write(base64.b64decode(message.split('base64,')[1]))
            if Post.objects.filter(slug=text_slug):
                return render(request, 'blog/new_film.html', {'form': form, 'loggined': True})
            Post_to_personal = Post.objects.create(title=returned['Title'], slug=text_slug,
                                                   description=returned['description'], author='darklorian',
                                                   style=returned['style'])
            for one_in_actors in request.POST.getlist('kinput_name_2'):
                selected_actors = Actors.objects.create(name=one_in_actors)
                Post_to_personal.actors.add(selected_actors)
            for one_in_prods in request.POST.getlist('kinput_name'):
                selected_producer = Prod.objects.create(name=one_in_prods)
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
        id_post = Post.objects.filter(slug=post).first()
        if id_post is not None:
            id_post.delete()
        entire = Entire_rating.objects.filter(name=id_post).first()
        if entire is not None:
            entire.delete()
        Rating.objects.filter(name=id_post).delete()
        logger_mini.logger(request.Auth_user, 'REMOVE POST', f'{post}')
        return redirect('/')


class One_Post(View):
    form = RatingForm

    def get(self, request, post):
        integ, integ_sum, dict_for_sum, form = 0, 0, {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, 'all': 0}, True
        poster, user = get_object_or_404(Post, slug=post), request.Auth_user
        rating_all = Rating.objects.filter(name=poster)
        rating_for_this_post = Entire_rating.objects.filter(name=poster).first()
        one_in_actors_list, one_in_prods_list = [], []
        for rating in rating_all:
            dict_for_sum[str(rating.stars)] = dict_for_sum[str(rating.stars)] + 1
            integ += int(rating.stars)
            integ_sum += 1
        if integ_sum != 0:
            dict_for_sum['all'] = integ / integ_sum
        for dict_in_actors in poster.actors.values():
            one_in_actors_list.append(list(dict_in_actors.values())[1])
        for dict_in_producers in poster.producer.values():
            one_in_prods_list.append(list(dict_in_producers.values())[1])
        if rating_for_this_post is None:
            Entire_rating.objects.create(name=poster, entire_stars=dict_for_sum['all'])
        else:
            rating_for_this_post.entire_stars = dict_for_sum['all']
            rating_for_this_post.save()
        actors = ', '.join(one_in_actors_list)
        producers = ', '.join(one_in_prods_list)
        form = True
        if Rating.objects.filter(username=user, name=poster).first() is None:
            form = self.form()
        return render(request, 'blog/detail.html',
                      {'post': poster, 'actors': actors, 'prods': producers, 'admin': request.Is_Anypermissions,
                       'form': form, 'RatingAll': dict_for_sum})

    def post(self, request, post):
        form = self.form(request.POST)
        poster = get_object_or_404(Post, slug=post)
        if form.is_valid():
            stars = form.cleaned_data
            Rating.objects.create(name=poster, username=request.Auth_user, stars=stars['like'])
            return redirect(f'/{post}')
