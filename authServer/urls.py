from django.urls import path
from . import views
app_name = 'videosserver'

urlpatterns = [
    path('login/', views.auth, name='authentication'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('add_admin/', views.add_admin, name='new_admin'),
    path('profile/', views.profile, name='profile'),
    path('add_moderator/', views.add_moderator, name='new_moderator'),
    path('delete_user/', views.del_user, name='delete_user'),
    path('del_moderator/', views.del_moderator, name='delete_moderator'),
    path('del_administrator/', views.del_administrator, name='delete_administrator')
]
