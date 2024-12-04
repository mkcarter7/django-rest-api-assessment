from django.db import models  # Import base class from Django stdlib
from .song import Song
from .genre import Genre

class SongGenre(models.Model):  # Must inherit from this base class
    song_id = models.ForeignKey(Song, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
