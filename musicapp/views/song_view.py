from rest_framework import viewsets, status
from musicapp.serializers import SongSerializer
from musicapp.models import Song, Musician
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from musicapp.models import Award, Rank, Ranking, User
from datetime import datetime


class SongView(viewsets.ModelViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.all()

    def create(self, request, *args, **kwargs):
        # list of musicians from the request
        musicians_id_list = request.data.get('musicians', [])
        # convert to int the ids
        musicians_ids = [int(musician_id) for musician_id in musicians_id_list]
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

        profile = request.data.get('profile')
        user = User.objects.get(id=profile)

        date_str = request.data.get('start_date')
        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        date_str_2 = request.data.get('end_date')
        date_2 = datetime.strptime(date_str_2, "%Y-%m-%dT%H:%M:%S.%fZ")

        start_formatted_date = date.strftime("%Y-%m-%d")
        end_formatted_date = date_2.strftime("%Y-%m-%d")

        song_data = {
            'name': request.data.get('name'),
            'gem': request.data.get('gem'),
            'start_date': start_formatted_date,
            'end_date': end_formatted_date,
            'week': request.data.get('week'),
            'release_year': request.data.get('release_year'),
            'genre': request.data.get('genre'),
            'album': request.data.get('album'),
            'youtube': request.data.get('youtube'),
            'profile': user
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


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_songs(request):
    songs = Song.objects.filter(profile=request.user).order_by('-week')
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def last_week(request):
    if Song.objects.exists():
        last_song = Song.objects.filter(profile=request.user).latest('id')
        week = last_song.week + 1
    else:
        week = 1

    return Response({'week': week})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_musicians(request):
    musician_updates = request.data.get("musicianUpdates", [])

    week = request.data.get("value_week")
    start_date_str_format = request.data.get("start_date")
    end_date_str_format = request.data.get("end_date")

    start_date = datetime.strptime(start_date_str_format, "%Y-%m-%dT%H:%M:%S.%fZ")
    end_date = datetime.strptime(end_date_str_format, "%Y-%m-%dT%H:%M:%S.%fZ")

    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    for musician_update in musician_updates:
        musician_id = musician_update['id']
        points_to_add = musician_update['pointsToAdd']
        musician = Musician.objects.get(id=musician_id)
        musician.points += int(points_to_add)
        musician.points_year += int(points_to_add)
        musician.points_semester += int(points_to_add)
        musician.save()

        award = Award.objects.create(
            type_award=1,
            description=f"Award {week}",
            points=int(points_to_add),
        )
        musician.awards.add(award)

        week_awards = musician.awards.filter(type_award=1)
        total_points = sum([award.points for award in week_awards])
        if week_awards:
            rating = total_points / len(week_awards)
        else:
            rating = 0

        musician.rating = rating
        musician.save()

    musicians = Musician.objects.filter(profile=request.user)
    musicians_sorted = sorted(musicians, key=lambda musician_x: musician_x.points, reverse=True)

    for position, musician in enumerate(musicians_sorted, start=1):
        musician.current_position = position
        musician.save()

        Rank.objects.create(
            week=week,
            position=position,
            musician=musician
        )

        if musician.best_position == 0 or musician.current_position < musician.best_position:
            musician.best_position = musician.current_position
            musician.start_date_best_position = start_date_str
            musician.end_date_best_position = end_date_str
            musician.save()

    if start_date.month == 6 and 21 <= start_date.day <= 27:
        top_10_musicians = Musician.objects.filter(profile=request.user).order_by('-points_semester')[:10]
        year = start_date.year

        for musician in top_10_musicians:
            Ranking(
                period="Semester 1 - " + str(year),
                points=musician.points_semester,
                musician=musician,
                profile=request.user
            ).save()

        top_10_musicians_year = Musician.objects.filter(profile=request.user).order_by('-points_year')[:10]
        year_before = year - 1

        for musician in top_10_musicians_year:
            Ranking(
                period="Period - " + str(year_before) + " - " + str(year),
                points=musician.points_year,
                musician=musician,
                profile=request.user
            ).save()

        Musician.objects.filter(profile=request.user).update(points_semester=0)
        Musician.objects.filter(profile=request.user).update(points_year=0)

    if start_date.month == 12 and 22 <= start_date.day <= 28:
        top_10_musicians = Musician.objects.filter(profile=request.user).order_by('-points_semester')[:10]
        year = start_date.year

        for musician in top_10_musicians:
            Ranking(
                period="Semester 2 - " + str(year),
                points=musician.points_semester,
                musician=musician,
                profile=request.user
            ).save()

        Musician.objects.filter(profile=request.user).update(points_semester=0)

    return Response({'message': 'Musicians updated successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_song_by_id(request,song_id):
    song = Song.objects.filter(profile=request.user).get(id=song_id)
    serializer = SongSerializer(song)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_songs_by_musician(request, musician_id):
    musician = Musician.objects.filter(profile=request.user).get(id=musician_id)
    songs = Song.objects.filter(profile=request.user,musicians=musician)
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data)