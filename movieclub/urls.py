from django.urls import path
from django.contrib.auth.models import User
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('account', views.account, name='account'),
    path('enter', views.inicio, name='inicio'),
    path('exit', views.log_out, name='log_out'),
    path('movies/<int:pelicula>', views.movpage, name='movpage'),
    path('psearch', views.psearch, name='psearch'),
    path('manage', views.manage, name='manage'),
    path('manage/movies', views.manmov, name='manmov'),
    path('delmov/<int:pelicula>', views.delmov, name='delmov'),
    path('manage/movies/edit/<int:pelicula>', views.filmform, name='filmform'),
    path('manage/movies/process/<int:pelicula>', views.p_filmform, name='p_filmform'),
    path('manage/users', views.manuser, name='manuser'),
    path('deluser/<int:user>', views.deluser, name='deluser'),
    path('manage/users/edit/<int:user>', views.userform, name='userform'),
    path('manage/users/process/<int:user>', views.p_userform, name='p_userform')
]
