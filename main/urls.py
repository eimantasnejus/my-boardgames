from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('boardgames/', views.BoardgameListView.as_view(), name='boardgames'),
    re_path(r'^boardgame/(?P<pk>\d+)$', views.BoardgameDetailView.as_view(), name='boardgame-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    path('playthroughs/', views.UserPlaythroughListView.as_view(), name='playthroughs'),
    path('playthrough_create/', views.playthrough_create_view, name='playthrough-create'),
    re_path(r'^playthrough/(?P<pk>[0-9A-Za-z\-]+)/$',
            views.UserPlaythroughDetailView.as_view(),
            name='playthrough-detail'),
    path('search/', views.search_by_name, name='search-by-name'),
    path('search/?<bgg_id>', views.search_by_id, name='search-by-id'),
]
