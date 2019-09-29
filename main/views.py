import re
import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render
from django.views import generic
from main.models import Boardgame, Author, Playthrough, Genre, Location


def clean_html(raw_html):
    cleaner = re.compile('<.*?>')
    clean_text = re.sub(cleaner, ' ', raw_html)
    return clean_text


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


def search_by_name(request):
    url = "https://www.boardgamegeek.com/xmlapi/search"
    querystring = {"search": request.GET.get('name')}
    headers = {
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    root = ET.ElementTree(ET.fromstring(response.text)).getroot()
    data = []
    for boardgame in root:
        bgg_id = boardgame.attrib.get('objectid')
        name = boardgame.find('name').text
        year = boardgame.find('yearpublished').text if boardgame.find('yearpublished') is not None else "-"
        data.append({
            'name': name,
            'year': year,
            'bgg_id': bgg_id
        })
    context = {
        'name': request.GET.get('name'),
        'data': data
    }
    return render(request, 'main/search_by_name.html', context)


def search_by_id(request, bgg_id):
    url = "https://www.boardgamegeek.com/xmlapi/game/" + bgg_id
    querystring = {"search": request.GET.get('id')}
    headers = {
        'cache-control': "no-cache",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    root = ET.ElementTree(ET.fromstring(response.text)).getroot()
    data = []
    for boardgame in root:
        name = boardgame.find('name').text
        year = boardgame.find('yearpublished').text if boardgame.find('yearpublished') is not None else "-"
        description = clean_html(boardgame.find('description').text)
        image_url = boardgame.find('image').text
        data.append({
            'name': name,
            'year': year,
            'description': description,
            'image_url': image_url,
        })
    context = {
        'data': data
    }
    return render(request, 'main/search_by_id.html', context)


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
