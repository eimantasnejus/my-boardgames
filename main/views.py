from django.shortcuts import render
from main.models import Boardgame, Author, Playthrough, Genre


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_boardgames = Boardgame.objects.all().count()
    num_playthroughs = Playthrough.objects.all().count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()

    context = {
        'num_books': num_boardgames,
        'num_instances': num_playthroughs,
        'num_authors': num_authors,
        'num_genres': num_genres,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
