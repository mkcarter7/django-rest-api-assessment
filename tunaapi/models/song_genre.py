from django.db import models  # Import base class from Django stdlib
from .song import Song
from .genre import Genre

class SongGenre(models.Model):  # Must inherit from this base class
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="songgenres")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="genresongs")
