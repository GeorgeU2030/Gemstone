from rest_framework import viewsets, status
from musicapp.serializers import SongSerializer
from musicapp.models import Song, Musician
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class SongView(viewsets.ModelViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.all()

    def create(self, request, *args, **kwargs):
        # list of musicians from the request
        musicians_id_list = request.data.get('musicians', [])
        # convert to int the ids
        musicians_ids = [int(musician_id) for musician_id in musicians_id_list.split(',')]
        # Verify at least one musician is provided
        if not musicians_ids:
            return Response({'error': 'At least one musician is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Verify all musicians exist
        for musician_id in musicians_ids:
            try:
                musician_id = Musician.objects.get(id=musician_id)
            except Musician.DoesNotExist:
                return Response({'error': f'Musician with id {musician_id} does not exist'},
                                status=status.HTTP_400_BAD_REQUEST)

        # Here is the creation of the Song

        song_data = {
            'name': request.data.get('name'),
            'gem': request.data.get('gem'),
            'start_date': request.data.get('start_date'),
            'end_date': request.data.get('end_date'),
            'week': request.data.get('week'),
            'release_year': request.data.get('release_year'),
            'genre': request.data.get('genre'),
            'album': request.data.get('album'),
            'youtube': request.data.get('youtube'),
        }

        song = Song.objects.create(**song_data)
        # associate musicians with the Song
        song.musicians.set(musicians_ids)

        serializer = self.get_serializer(song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def latest_song(request):
    song = Song.objects.filter(profile=request.user).order_by('-id').first()

    if song:
        serializer = SongSerializer(song)
        return Response(serializer.data)
    else:
        return Response({'error': 'No songs found'}, status=status.HTTP_404_NOT_FOUND)
