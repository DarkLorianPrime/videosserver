from django.urls import path
from . import views
app_name = 'videosserver'

urlpatterns = [
    path('login/', views.auth, name='authentication'),
    path('registration/', views.registration, name='registration'),
    path('logout/', views.logout, name='logout'),
    path('add_admin/', views.add_admin, name='new_admin'),
    path('profile/', views.profile, name='profile')
]
