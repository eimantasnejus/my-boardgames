from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('boardgames/', views.BoardgameListView.as_view(), name='boardgames'),
    re_path(r'^boardgame/(?P<pk>\d+)$', views.BoardgameDetailView.as_view(), name='boardgame-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
]
