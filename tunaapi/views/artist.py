"""View module for handling requests about types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist
from tunaapi.models import Song


class ArtistView(ViewSet):
    """Tuna Api Artist view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single Artist

        Returns:
            Response -- JSON serialized Artist
        """
        try:
            artist = Artist.objects.get(pk=pk)
            song_count = Song.objects.filter(artist=artist).count()
            artist.song_count = song_count
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all Artists

        Returns:
            Response -- JSON serialized list of Artists
        """
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized arist instance
        """

        artist = Artist.objects.create(
        name=request.data["name"],
        age=request.data["age"],
        bio=request.data["bio"],
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for an artist

        Returns:
        Response -- Empty body with 204 status code
        """

        artist = Artist.objects.get(pk=pk)
        artist.name=request.data["name"]
        artist.age=request.data["age"]
        artist.bio=request.data["bio"]
        artist.save()
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def destroy(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    song_count = serializers.SerializerMethodField()
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')
        depth = 1
        
    def get_song_count(self, obj):
        return obj.songs.count()
        
class SingleArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artist types
    """
    song_count = serializers.IntegerField(default=None)
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')
        depth = 1
       
    def get_song_count(self, obj):
        return obj.songs.count()
