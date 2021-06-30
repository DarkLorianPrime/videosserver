from django.urls import path

from Blog.views import Recent_Password, Recent_Password_local
from . import views
app_name = 'videosserver'

urlpatterns = [
    path('login/', views.Auth.as_view(), name='authentication'),
    path('registration/', views.Registration.as_view(), name='registration'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('add_admin/', views.Add_Admin.as_view(), name='new_admin'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('add_moderator/', views.Add_Moderator.as_view(), name='new_moderator'),
    path('delete_user/', views.Delete_User.as_view(), name='delete_user'),
    path('del_moderator/', views.Delete_Moderators.as_view(), name='delete_moderator'),
    path('del_administrator/', views.Delete_Administrator.as_view(), name='delete_administrator'),
    path('recent/', Recent_Password.as_view(), name='RecentPassword'),
    path('recent/<str:request_token>/', Recent_Password_local.as_view(), name='RecentPasswordLocal')
]
