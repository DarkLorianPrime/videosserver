import requests
from django.shortcuts import render, get_object_or_404, redirect

from Blog import models
from Blog.Form import FilmForm, NewNameForm
from Blog.models import Post
from extras.check_person import get_login


def new_prod(request):
    text = get_login(request)
    login_name = False
    if text is not False:
        login_name = text[0].username
    if text[1] is False:
        return render(request, 'blog/post/new_prod.html', {'error': True})
    if request.method == 'POST':
        form = NewNameForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            filters = models.prod.objects.filter(name=returned['Name']).first()
            if filters is not None:
                return render(request, 'blog/post/new_prod.html', {'form': form, 'loggined': True})
            models.prod(name=returned['Name']).save()
            return redirect('/')
    form = NewNameForm()
    return render(request, 'blog/post/new_prod.html', {'form': form, 'who': 'producer', 'login_name': login_name})


def new_actor(request):
    text = get_login(request)
    login_name = False
    if text is not False:
        login_name = text[0].username
    if text[1] is False:
        return render(request, 'blog/post/new_prod.html', {'error': True})
    if request.method == 'POST':
        form = NewNameForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            filters = models.actors.objects.filter(name=returned['Name']).first()
            if filters is not None:
                return render(request, 'blog/post/new_prod.html', {'form': form, 'loggined': True})
            models.actors(name=returned['Name']).save()
            return redirect('/')
    form = NewNameForm()
    return render(request, 'blog/post/new_prod.html', {'form': form, 'who': 'actor', 'login_name': login_name})


def new_film(request):
    dictes_for_actors, dictes_for_prods, z = {}, {}, 0
    text = get_login(request)
    login_name = False
    if text is not False:
        login_name = text.username
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            if Post.objects.filter(slug=returned['slug']):
                return render(request, 'blog/post/new_film.html', {'form': form, 'loggined': True})
            for i in returned['actors']:
                dictes_for_actors[str(z)] = str(i)
                z += 1
            z = 0
            for i in returned['prod']:
                dictes_for_prods[str(z)] = str(i)
                z += 1
            photo = returned['art_link']
            if returned['art_link'] == '':
                photo = requests.get(f'https://imdb-api.com/API/SearchTitle/k_hfcfkmgb/{returned["Title"]}').json()[
                    'results'][
                    0]['image']
            models.Post(title=returned['Title'], producer=dictes_for_prods, actors=dictes_for_actors,
                        slug=returned['slug'], description=returned['description'], author='darklorian', art_link=photo,
                        style=returned['style']).save()
            return redirect('/')
    form = FilmForm()
    return render(request, 'blog/post/new_film.html', {'form': form, 'login_name': login_name})


def post_list(request):
    post_listin = Post.objects.all()
    text = get_login(request)
    login_name = False
    if text is not False:
        login_name = text[0]
    return render(request, 'blog/post/list.html', {'posts': post_listin, 'login_name': login_name})


def post_one(request, post):
    post, text = get_object_or_404(Post, slug=post), get_login(request)
    login_name = False
    if text[0] is not False:
        login_name = text[0].username
    f, g = [], []
    for i in post.producer.values():
        f.append(i)
    for i in post.actors.values():
        g.append(i)
    s, z = ', '.join(f), ', '.join(g)
    return render(request, 'blog/post/detail.html', {'post': post, 'login_name': login_name, 'actors': z, 'prods': s})
