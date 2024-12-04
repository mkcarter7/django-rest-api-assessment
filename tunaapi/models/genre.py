from django.db import models  # Import base class from Django stdlib


class Genre(models.Model):  # Must inherit from this base class
    description = models.CharField(max_length=100)  # Define all non-id fields
