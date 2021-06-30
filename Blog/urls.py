from django.urls import path
from . import views

app_name = 'Blog_list'

urlpatterns = [
    path('filters/', views.Filter.as_view(), name='filters'),
    path('', views.Post_List.as_view(), name='post_list'),
    path('<slug:post>/', views.One_Post.as_view(), name='post_one'),
    path('<slug:post>/delete', views.Post_Delete.as_view(), name='post_one_delete'),
    path('add_film', views.New_Film.as_view(), name='new_film'),
    path('add_style', views.New_Style.as_view(), name='new_style'),
    path('moderPanel', views.Moder_Panel.as_view(), name='moderPanel'),
    path('adminPanel', views.Admin_Panel.as_view(), name='adminPanel'),
    path('resetPassword', views.Reset_Password.as_view(), name='resetPassword'),
]