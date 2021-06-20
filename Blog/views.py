import requests
import transliterate
from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext

from Blog.Form import FilmForm, NewNameForm, NewStyleForm, RatingForm, FiltersForm
from Blog.models import Post, Rating, Actors, Prod, Styles
from extras.replacer import replacer


def new_producers(request):
    form = NewNameForm()
    if not request.Is_Anypermissions:
        return render(request, 'blog/post/new_prod.html', {'error': True})
    if request.method == 'POST':
        form = NewNameForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            filters = Prod.objects.filter(name=returned['Name']).first()
            if filters is not None:
                return render(request, 'blog/post/new_prod.html', {'form': form, 'loggined': True})
            Prod.objects.create(name=returned['Name'])
    return render(request, 'blog/post/new_prod.html',
                  {'form': form, 'who': 'producer', 'admin': True})


def new_actor(request):
    form = NewNameForm()
    if not request.Is_Anypermissions:
        return render(request, 'blog/post/new_prod.html', {'error': True})
    if request.method == 'POST':
        form = NewNameForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            filters = Actors.objects.filter(name=returned['Name']).first()
            if filters is not None:
                return render(request, 'blog/post/new_prod.html',
                              {'form': form, 'loggined': True, 'admin': True, 'who': 'actor'})
            Actors.objects.create(name=returned['Name'])
    return render(request, 'blog/post/new_prod.html',
                  {'form': form, 'who': 'actor', 'admin': True})


def moderPanel(request):
    if not request.Is_Anypermissions:
        return render(request, 'blog/post/moderPanel.html', {'error': True})
    return render(request, 'blog/post/moderPanel.html', {'admin': True})


def adminPanel(request):
    if not request.is_administrator:
        return render(request, 'blog/post/adminPanel.html', {'error': True})
    return render(request, 'blog/post/adminPanel.html', {'admin': True})


def new_style(request):
    admin, form = False, NewStyleForm()
    if not request.Is_Anypermissions:
        return render(request, 'blog/post/new_film.html', {'error': True})
    if request.method == 'POST':
        form = NewStyleForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            if Styles.objects.filter(style=returned['Name']).first() is not None:
                return render(request, 'blog/post/new_prod.html',
                              {'form': form, 'loggined': True, 'admin': True, 'who': 'style'})
            Styles.objects.create(style=returned['Name'])
    return render(request, 'blog/post/new_prod.html', {'admin': True, 'form': form, 'who': 'style'})


def filters(request):
    form, actor, prod, er_l, list_find = FiltersForm(), False, False, False, []
    if request.method == 'POST':
        form = FiltersForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if form_data['names'] != '':
                returned = Post.objects.filter(title__startswith=form_data['names']).first()
                if returned is not None:
                    return redirect(f'/{returned.slug}')
                else:
                    er_l = True
                return render(request, 'blog/post/filters.html',
                              {'form': form, 'admin': request.Is_Anypermissions, 'error_local': er_l})
            list_find = Post.objects.all().filter(producer=form_data['producer'], actors=form_data['actor'])
            return render(request, 'blog/post/list.html', {'posts': list_find, 'admin': request.Is_Anypermissions})
    return render(request, 'blog/post/filters.html',
                  {'form': form, 'admin': request.Is_Anypermissions, 'error_local': er_l})


def new_film(request):
    dictes_for_Actors, dictes_for_prods, int_for_actors, int_for_prods, form, admin = {}, {}, 0, 0, FilmForm(), False
    if not request.Is_Anypermissions:
        return render(request, 'blog/post/new_film.html', {'error': True})
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            photo = 'https://i2.wp.com/dimlix.com/wp-content/uploads/2020/07/150-scaled.jpg'
            if returned['art_link'] == '':
                link = f'https://imdb-api.com/API/SearchTitle/k_hfcfkmgb/{returned["Title"]}'
                photo = requests.get(link).json()['results']
                if photo:
                    photo = photo[0]['image']
            text_for_slug = transliterate.translit(returned['Title'], 'ru', reversed=True)
            text_slug = replacer(text_for_slug)
            if Post.objects.filter(slug=text_slug):
                return render(request, 'blog/post/new_film.html', {'form': form, 'loggined': True})
            Post_to_personal = Post.objects.create(title=returned['Title'], slug=text_slug, art_link=photo,
                                                   description=returned['description'], author='darklorian',
                                                   style=returned['style'])
            for one_in_actors in returned['actors']:
                selected_actors = Actors.objects.filter(name=one_in_actors).first()
                Post_to_personal.actors.add(selected_actors)
            for one_in_prods in returned['prod']:
                selected_producer = Prod.objects.filter(name=one_in_prods).first()
                Post_to_personal.producer.add(selected_producer)
            return redirect('/')
    return render(request, 'blog/post/new_film.html', {'form': form, 'admin': True})


def post_list(request):
    post_listin = Post.objects.all()
    return render(request, 'blog/post/list.html', {'posts': post_listin, 'admin': request.Is_Anypermissions})


def post_one_delete(request, post):
    post_delete = Post.objects.filter(slug=post).first()
    post_delete.delete()
    return redirect('/')


def post_one(request, post):
    integ, integ_sum, dict_for_sum = 0, 0, {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    form = RatingForm()
    poster, user = get_object_or_404(Post, slug=post), request.Auth_user
    rating_user = Rating.objects.filter(name=post, username=user).first()
    if rating_user is None:
        if request.method == 'POST':
            form = RatingForm(request.POST)
            if form.is_valid():
                stars = form.cleaned_data
                Rating.objects.create(name=post, username=user, stars=stars['like'])
    else:
        form = True
    rating_all = Rating.objects.all().filter(name=post)
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
    actors = ', '.join(one_in_actors_list)
    producers = ', '.join(one_in_prods_list)
    return render(request, 'blog/post/detail.html',
                  {'post': poster, 'actors': actors, 'prods': producers, 'admin': request.Is_Anypermissions,
                   'form': form, 'RatingAll': dict_for_sum})
