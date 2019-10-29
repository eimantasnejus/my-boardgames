import uuid  # Required for unique book instances

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns

class Category(models.Model):
    """Model representing boardgame category."""
    name = models.TextField(max_length=100)
    bgg_id = models.IntegerField(null=True)

class Genre(models.Model):
    """Model representing a board game genre."""
    name = models.CharField(max_length=200, help_text='Enter a board game genre (e.g. Roll of the Die)')
    bgg_id = models.IntegerField(null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Location(models.Model):
    """Model representing a place or address"""
    address = models.CharField(max_length=200, help_text='Enter a board game genre (e.g. Roll of the Die)')

    def __str__(self):
        """String for representing the Model object."""
        return self.address


class Player(models.Model):
    """Model representing a friend, participating in playthrough."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        """String for representing the Model object."""
        return ' '.join([self.first_name, self.last_name])


class Boardgame(models.Model):
    """Model representing a general board game."""
    name = models.CharField(max_length=200)
    year_published = models.IntegerField(null=True)
    min_players = models.IntegerField(null=True)
    max_players = models.IntegerField(null=True)
    min_playtime = models.IntegerField(null=True)
    max_playtime = models.IntegerField(null=True)
    image_url = models.TextField(max_length=1000, null=True)
    thumbnail_url = models.TextField(max_length=1000, null=True)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the board game')
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this board game')
    bgg_overall_rating = models.IntegerField(null=True)
    bgg_id = models.IntegerField(null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this board game."""
        return reverse('boardgame-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class Playthrough(models.Model):
    """Model representing a playthrough of one game."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Unique ID for this playthrough')
    boardgame = models.ForeignKey(Boardgame, on_delete=models.SET_NULL, null=True)
    datetime = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    players = models.ManyToManyField(Player, help_text='Add players who participate in this game.')
    playtime = models.FloatField(null=True)
    # TODO: bool - explaining rules
    # TODO: score - each player

    class Meta:
        ordering = ['datetime']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.datetime} ({self.boardgame.name})'

    def get_absolute_url(self):
        """Returns the url to access a detail record for this playthrough."""
        return reverse('playthrough-detail', args=[str(self.id)])


class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
