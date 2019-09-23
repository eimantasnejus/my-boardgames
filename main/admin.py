from django.contrib import admin
from main.models import Boardgame, Author, Playthrough, Genre

admin.site.register(Boardgame)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Playthrough)
