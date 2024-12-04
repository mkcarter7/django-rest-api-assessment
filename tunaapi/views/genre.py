"""View module for handling requests about types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Genre, genre


class GenreView(ViewSet):
    """ types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single type
        
        Returns:
            Response -- JSON serialized type
        """
        try:
            song = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(song)
            return Response(serializer.data)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all game types

        Returns:
            Response -- JSON serialized list of game types
        """
        genres = genre.objects.all()
        
        serializer = GenreSerializer(genre, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized instance
        """
        genre = genre.objects.create(
            description=request.data["description"],
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data)
    
    def update(self, request, pk):
        """Handle PUT requests for an event

        Returns
            Response -- Empty body with 204 status code
        """

        genre = genre.objects.get(pk=pk)
        genre.id = genre.id
        genre.description = request.data["description"]
        
        genre.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        genre = genre.objects.get(pk=pk)
        genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
            
class GenreSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    class Meta:
        model = genre
        fields = ('id', 'description')
        depth = 1
