from django.urls import path
from . import views

app_name = 'Blog_list'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<slug:post>/', views.post_one, name='post_one'),
    path('loggined', views.get_login, name='get_login'),
    path('add_film', views.new_film, name='new_film'),
    path('add_producer', views.new_prod, name='new_prod'),
    path('add_actor', views.new_actor, name='new_actor'),
    path('add_style', views.new_style, name='new_style')
]