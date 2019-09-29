from django.shortcuts import render
from django.views import generic
from main.models import Boardgame, Author, Playthrough, Genre, Location


def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_boardgames = Boardgame.objects.all().count()
    num_playthroughs = Playthrough.objects.all().count()
    num_authors = Author.objects.count()
    num_genres = Genre.objects.count()
    num_locations = Location.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_boardgames,
        'num_instances': num_playthroughs,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_locations': num_locations,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class BoardgameListView(generic.ListView):
    model = Boardgame
    paginate_by = 10


class BoardgameDetailView(generic.DetailView):
    model = Boardgame
    paginate_by = 10


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
    paginate_by = 10
