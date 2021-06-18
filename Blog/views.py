import requests
from django.shortcuts import render, get_object_or_404, redirect

from Blog.Form import FilmForm, NewNameForm, NewStyleForm, RatingForm, FiltersForm
from Blog.models import Post, Rating, Actors, Prod, Styles
from extras.authentication import BackendAuth


def new_prod(request):
    form = NewNameForm()
    if not request.Is_Anypermissions:
        return render(request, 'blog/post/new_prod.html', {'error': True})
    if request.method == 'POST':
        form = NewNameForm.objects.create(request.POST)
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
        form = NewNameForm.objects.create(request.POST)
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
    form, actor, prod, admin, er_l, list_find = FiltersForm(), False, False, False, False, []
    if not request.Is_Anypermissions:
        admin = True
    if request.method == 'POST':
        form = FiltersForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['names'] != '':
                returned = Post.objects.filter(title__startswith=cd['names']).first()
                if returned is not None:
                    return redirect(f'/{returned.slug}')
                else:
                    er_l = True
            all_posts = Post.objects.all()
            for i in all_posts:
                for z in i.Actors.values():
                    if z == str(cd['actor']):
                        list_find.append(i)
                for z in i.producer.values():
                    if z == str(cd['producer']):
                        if i in list_find:
                            continue
                        list_find.append(i)
            if list_find:
                return render(request, 'blog/post/list.html', {'posts': list_find})
    return render(request, 'blog/post/filters.html',
                  {'form': form, 'admin': admin, 'error_local': er_l})


def new_film(request):
    dictes_for_Actors, dictes_for_prods, int_for_actors, int_for_prods, form, admin = {}, {}, 0, 0, FilmForm(), False
    if not request.Is_Anypermissions:
        return render(request, 'blog/post/new_film.html', {'error': True})
    if request.method == 'POST':
        form = FilmForm(request.POST)
        if form.is_valid():
            returned = form.cleaned_data
            if Post.objects.filter(slug=returned['slug']):
                return render(request, 'blog/post/new_film.html', {'form': form, 'loggined': True})
            for one_in_actors in returned['actors']:
                dictes_for_Actors[str(int_for_actors)] = str(one_in_actors)
                int_for_actors += 1
            for one_in_prods in returned['prod']:
                dictes_for_prods[str(int_for_prods)] = str(one_in_prods)
                int_for_prods += 1
            photo = returned['art_link']
            if returned['art_link'] == '':
                photo = requests.get(f'https://imdb-api.com/API/SearchTitle/k_hfcfkmgb/{returned["Title"]}').json()[
                    'results']
                if photo:
                    photo = photo[0]['image']
            Post.objects.create(title=returned['Title'], producer=dictes_for_prods, actors=dictes_for_Actors,
                                slug=returned['slug'], description=returned['description'], author='darklorian',
                                art_link=photo, style=returned['style'])
            return redirect('/')
    return render(request, 'blog/post/new_film.html', {'form': form, 'admin': True})


def post_list(request):
    post_listin = Post.objects.all()
    admin = False
    if request.Is_Anypermissions:
        admin = True
    return render(request, 'blog/post/list.html', {'posts': post_listin, 'admin': admin})


def post_one_delete(request, post):
    post.delete()
    return redirect('/')


def post_one(request, post):
    integ, integ_sum, dict_for_sum = 0, 0, {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    form = RatingForm()
    poster, user = get_object_or_404(Post, slug=post), request.Auth_user
    admin = False
    if request.Is_Anypermissions:
        admin = True
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
    for rating in rating_all:
        dict_for_sum[str(rating.stars)] = dict_for_sum[str(rating.stars)] + 1
        integ += int(rating.stars)
        integ_sum += 1
    if integ_sum != 0:
        dict_for_sum['all'] = integ / integ_sum
    Actors_list, producers_list = [], []
    for i in poster.producer.values():
        producers_list.append(i)
    for i in poster.actors.values():
        Actors_list.append(i)
    producers, actors = ', '.join(producers_list), ', '.join(Actors_list)
    return render(request, 'blog/post/detail.html',
                  {'post': poster, 'Actors': actors, 'prods': producers, 'admin': admin,
                   'form': form, 'RatingAll': dict_for_sum})
