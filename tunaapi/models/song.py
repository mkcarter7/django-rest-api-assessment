from django.db import models  # Import base class from Django stdlib
from .artist import Artist

class Song(models.Model):  # Must inherit from this base class
    title = models.CharField(max_length=75)  # Define all non-id fields
    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    album = models.CharField(max_length=75)
    length = models.PositiveSmallIntegerField()
