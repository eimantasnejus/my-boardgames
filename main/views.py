import ast
import re
import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render
from django.views import generic
from main.forms import PlaythroughForm
from main.models import Boardgame, Author, Playthrough, Genre, Location


def clean_html(raw_html):
    cleaner = re.compile('<.*?>|&.*?;')
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


def get_boardgame_dict(xml, *args):
    """Return boardgame_dict, filled with key - value pairs extracted from xml."""
    boardgame_dict = {
        'name': xml.findall("name[@primary='true']")[0].text,
        'bgg_id': xml.attrib.get('objectid')
    }
    for parameter in args:
        boardgame_dict.update({
            parameter: clean_html(xml.find(parameter).text) if xml.find(parameter) is not None else "-"
        })
    return boardgame_dict


def search_by_id(request, bgg_id):
    """Return rendered template representing selected information from bgg."""
    boardgame = {}
    if request.method == 'POST':
        context = {'request_type': 'POST'}
        boardgame = request.POST.get('boardgame')
        if boardgame:
            boardgame = ast.literal_eval(boardgame)
            if boardgame.get('bgg_id') and Boardgame.objects.filter(bgg_id=boardgame.get('bgg_id')):
                context.update({'status': 'existing'})
            else:
                Boardgame.objects.create(
                    name=boardgame.get('name'),
                    year_published=boardgame.get('yearpublished'),
                    min_players=boardgame.get('minplayers'),
                    max_players=boardgame.get('maxplayers'),
                    min_playtime=boardgame.get('minplaytime'),
                    max_playtime=boardgame.get('maxplaytime'),
                    image_url=boardgame.get('image'),
                    thumbnail_url=boardgame.get('thumbnail'),
                    summary=boardgame.get('description'),
                    bgg_id=boardgame.get('bgg_id')
                )
                context.update({'status': 'existing'})
    else:
        url = "https://www.boardgamegeek.com/xmlapi/game/" + bgg_id
        querystring = {"search": request.GET.get('id')}
        response = requests.request("GET", url, params=querystring)
        root = ET.ElementTree(ET.fromstring(response.text)).getroot()
        for boardgame_xml in root:
            boardgame_dict = get_boardgame_dict(boardgame_xml, 'yearpublished', 'minplayers', 'maxplayers',
                                                'minplaytime', 'maxplaytime', 'description', 'image', 'thumbnail')
            boardgame = boardgame_dict
        context = {'request_type': 'GET'}
    context.update({'boardgame': boardgame})
    return render(request, 'main/search_by_id.html', context)


def playthrough_create_view(request):
    """Form to register a new playthrough."""
    if request.method == 'GET':
        print("TRIGERED GET")
        form = PlaythroughForm(request.POST or None)
        if form.is_valid():
            form.save()
        context = {
            'form': form
        }
        return render(request, "main/playthrough_create.html", context)
    elif request.method == 'POST':
        print("TRIGERED POST")
        form = PlaythroughForm(request.POST or None)
        if form.is_valid():
            form.save()
        context = {
            'playthrough_list': Playthrough.objects.all()
        }
        return render(request, "main/playthrough_list.html", context)


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


class UserPlaythroughListView(generic.ListView):
    model = Playthrough
    queryset = Playthrough.objects.all()
    paginate_by = 10


class UserPlaythroughDetailView(generic.DetailView):
    model = Playthrough

    @staticmethod
    def get_boardgame_name(boardgame_id):
        """Return selected boardgame name."""
        return Boardgame.objects.get(pk=boardgame_id).name
