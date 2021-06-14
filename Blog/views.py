import requests
from django.shortcuts import render, get_object_or_404, redirect

from Blog import models
from Blog.Form import FilmForm, NewNameForm, NewStyleForm
from Blog.models import Post
from extras.check_person import get_login


def new_prod(request):
    form = NewNameForm()
    text = get_login(request)
    login_name = False
    if text[0] is not False:
        login_name = text[0].username
    if text[1] is False or text[2] is False:
        return render(request, 'blog/post/new_prod.html', {'error': True})
    if request.method == 'POST':
        form = NewNameForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            filters = models.prod.objects.filter(name=returned['Name']).first()
            if filters is not None:
                return render(request, 'blog/post/new_prod.html', {'form': form, 'loggined': True})
            models.prod(name=returned['Name']).save()
    return render(request, 'blog/post/new_prod.html', {'form': form, 'who': 'producer', 'login_name': login_name, 'admin': True})


def new_actor(request):
    form = NewNameForm()
    text = get_login(request)
    login_name = False
    if text[0] is not False:
        login_name = text[0].username
    if text[2] is False:
        return render(request, 'blog/post/new_prod.html', {'error': True})
    if request.method == 'POST':
        form = NewNameForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            filters = models.actors.objects.filter(name=returned['Name']).first()
            if filters is not None:
                return render(request, 'blog/post/new_prod.html', {'form': form, 'loggined': True, 'admin': True, 'who': 'actor', 'login_name': login_name})
            models.actors(name=returned['Name']).save()
    return render(request, 'blog/post/new_prod.html', {'form': form, 'who': 'actor', 'login_name': login_name, 'admin': True})


def moderPanel(request):
    text = get_login(request)
    login_name = False
    if text[0] is not False:
        login_name = text[0].username
    if text[2] is False:
        return render(request, 'blog/post/moderPanel.html', {'error': True})
    return render(request, 'blog/post/moderPanel.html', {'login_name': login_name, 'admin': True})


def adminPanel(request):
    text = get_login(request)
    login_name = False
    if text[0] is not False:
        login_name = text[0].username
    if text[1] is False:
        return render(request, 'blog/post/moderPanel.html', {'error': True})
    return render(request, 'blog/post/adminPanel.html', {'login_name': login_name, 'admin': True})


def new_style(request):
    login_name, admin, text, form = False, False, get_login(request), NewStyleForm()
    if text[0] is not False:
        login_name = text[0].username
    if text[1] is False:
        return render(request, 'blog/post/new_film.html', {'error': True})
    if request.method == 'POST':
        form = NewStyleForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            if models.styles.objects.filter(style=returned['Name']).first() is not None:
                return render(request, 'blog/post/new_prod.html', {'form': form, 'loggined': True, 'admin': True, 'who': 'style', 'login_name': login_name})
            models.styles(style=returned['Name']).save()
    return render(request, 'blog/post/new_prod.html', {'admin': True, 'login_name': login_name, 'form': form, 'who': 'style'})


def new_film(request):
    form = FilmForm()
    dictes_for_actors, dictes_for_prods, z, w = {}, {}, 0, 0
    text = get_login(request)
    login_name, admin = False, False
    if text[0] is not False:
        login_name = text[0].username
    if text[1] is False:
        return render(request, 'blog/post/new_film.html', {'error': True})
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            if Post.objects.filter(slug=returned['slug']):
                return render(request, 'blog/post/new_film.html', {'form': form, 'loggined': True})
            for i in returned['actors']:
                dictes_for_actors[str(z)] = str(i)
                z += 1
            for i in returned['prod']:
                dictes_for_prods[str(z)] = str(i)
                w += 1
            photo = returned['art_link']
            if returned['art_link'] == '':
                photo = requests.get(f'https://imdb-api.com/API/SearchTitle/k_hfcfkmgb/{returned["Title"]}').json()['results']
                print(photo)
                if photo:
                    photo = photo[0]['image']
            models.Post(title=returned['Title'], producer=dictes_for_prods, actors=dictes_for_actors,
                        slug=returned['slug'], description=returned['description'], author='darklorian', art_link=photo,
                        style=returned['style']).save()
            return redirect('/')
    return render(request, 'blog/post/new_film.html', {'form': form, 'login_name': login_name, 'admin': True})


def post_list(request):
    post_listin = Post.objects.all()
    text = get_login(request)
    login_name, admin = False, False
    if text[0] is not False:
        login_name = text[0]
    if text[1] is not False or text[2] is not False:
        admin = True
    return render(request, 'blog/post/list.html', {'posts': post_listin, 'login_name': login_name, 'admin': admin})


def post_one(request, post):
    post, text = get_object_or_404(Post, slug=post), get_login(request)
    login_name, admin = False, False
    if text[0] is not False:
        login_name = text[0].username
    if text[1] is not False or text[2] is not False:
        admin = True
        if request.method == 'POST':
            post = Post.objects.filter(slug=post).first()
            if post is not None:
                post.delete()
            return redirect('/')
    actors_list, producers_list = [], []
    print(post.producer.values())
    for i in post.producer.values():
        producers_list.append(i)
    for i in post.actors.values():
        actors_list.append(i)
    producers, actors = ', '.join(producers_list), ', '.join(actors_list)
    return render(request, 'blog/post/detail.html', {'post': post, 'login_name': login_name, 'actors': actors, 'prods': producers, 'admin': admin})
