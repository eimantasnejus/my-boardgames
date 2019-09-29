from django.contrib import admin
from main.models import Boardgame, Author, Playthrough, Genre, Location


class PlaythroughInline(admin.TabularInline):
    model = Playthrough
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')


@admin.register(Boardgame)
class BoardgameAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'display_genre')
    inlines = [PlaythroughInline]


@admin.register(Playthrough)
class PlaythroughAdmin(admin.ModelAdmin):
    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
