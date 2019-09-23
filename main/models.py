import uuid  # Required for unique book instances

from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns


class Genre(models.Model):
    """Model representing a board game genre."""
    name = models.CharField(max_length=200, help_text='Enter a board game genre (e.g. Roll of the Die)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Location(models.Model):
    """Model representing a place or address"""
    address = models.CharField(max_length=200, help_text='Enter a board game genre (e.g. Roll of the Die)')

    def __str__(self):
        """String for representing the Model object."""
        return self.address


class Boardgame(models.Model):
    """Model representing a general board game."""
    name = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the board game')
    # ManyToManyField used because genre can contain many board games. Board games can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this board game')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this board game."""
        return reverse('book-detail', args=[str(self.id)])


class Playthrough(models.Model):
    """Model representing a playthrough of one game."""
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='Unique ID for this playthrough')
    boardgame = models.ForeignKey(Boardgame, on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.date} ({self.boardgame.name})'


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
