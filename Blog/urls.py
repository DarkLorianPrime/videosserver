from django.urls import path
from . import views

app_name = 'Blog_list'

urlpatterns = [
    path('filters/', views.filters, name='filters'),
    path('', views.post_list, name='post_list'),
    path('<slug:post>/', views.post_one, name='post_one'),
    path('<slug:post>/delete', views.post_one_delete, name='post_one_delete'),
    path('loggined', views.get_login, name='get_login'),
    path('add_film', views.new_film, name='new_film'),
    path('add_producer', views.new_prod, name='new_prod'),
    path('add_actor', views.new_actor, name='new_actor'),
    path('add_style', views.new_style, name='new_style'),
    path('moderPanel', views.moderPanel, name='moderPanel'),
    path('adminPanel', views.adminPanel, name='adminPanel'),
]