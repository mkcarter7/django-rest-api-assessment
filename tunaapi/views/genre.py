"""View module for handling requests about types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre
from tunaapi.models import Song


class GenreView(ViewSet):
    """ types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single type
        
        Returns:
            Response -- JSON serialized type
        """
        try:
            genre = Genre.objects.get(pk=pk)
            songs = Song.objects.filter(songgenres__genre_id=genre)
            genre.songs=songs.all()
            serializer = SingleGenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized instance
        """
        genre = Genre.objects.create(
        description=request.data["description"],
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a genre

        Returns:
            Response -- Empty body with 204 status code
        """

        id = pk
        genre = Genre.objects.get(pk=pk)
        genre.description = request.data["description"]

        genre.save()

        serializer = GenreSerializer(genre)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
            
class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = Genre
        fields = ('id', 'description')
        depth = 1
        
class SongSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length')
        depth = 1

class SingleGenreSerializer(serializers.ModelSerializer):
        songs = SongSerializer(read_only=True, many=True)
        class Meta:
            model = Genre
            fields = ('id', 'description', 'songs')
            depth = 1
