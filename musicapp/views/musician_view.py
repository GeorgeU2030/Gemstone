from rest_framework import viewsets
from musicapp.serializers import MusicianSerializer, MusicianCreateSerializer, MusicianAwardSerializer
from musicapp.models import Award, Musician
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Count, Q


class MusicianView(viewsets.ModelViewSet):
    queryset = Musician.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MusicianCreateSerializer
        return MusicianSerializer


# get the id of the user
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_id_user(request):
    return Response(request.user.id)


# get the top 3 musicians with the most points
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def top_musicians_points(request):
    musicians = Musician.objects.filter(profile=request.user).order_by('-points')[:3]
    serializer = MusicianCreateSerializer(musicians, many=True)
    return Response(serializer.data)


# get the top 3 musicians with the most awards
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def top_musicians_awards(request):
    musicians = (Musician.objects.filter(profile=request.user)
                 .annotate(award_count=Count('awards'))
                 .order_by('-award_count')[:3])
    serializer = MusicianAwardSerializer(musicians, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ranking(request):
    musicians = Musician.objects.filter(profile=request.user).order_by('current_position')
    serializer = MusicianSerializer(musicians, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def ranking_awards(request):
    musicians = (Musician.objects.filter(profile=request.user)
                 .annotate(award_count=Count('awards'))
                 .order_by('-award_count', 'current_position'))
    serializer = MusicianSerializer(musicians, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_musician(request):
    search = request.query_params.get('search')

    if search == '':
        return Response([])

    musicians = Musician.objects.filter(profile=request.user).filter(Q(name__istartswith=search))
    serializer = MusicianSerializer(musicians, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_musician(request, musician_id):
    musician = Musician.objects.filter(profile=request.user).get(id=musician_id)
    serializer = MusicianSerializer(musician)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def all_musicians(request):
    musicians = Musician.objects.filter(profile=request.user)
    serializer = MusicianSerializer(musicians, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_points_week(request):
    musician_ids = request.data.get('musicianIds')
    points_to_add = request.data.get('pointsToAdd')

    if musician_ids and points_to_add:
        
        musicians = Musician.objects.filter(profile=request.user).filter(id__in=musician_ids)
        for musician in musicians:
            musician.points += points_to_add
            musician.points_semester += points_to_add
            musician.points_year += points_to_add
            musician.save()


    musicians = Musician.objects.filter(profile=request.user)

    musicians_sorted = sorted(musicians, key=lambda musician: musician.points, reverse=True)

    for position, musician in enumerate(musicians_sorted, start=1):
        musician.current_position = position
        musician.save()

        if musician.best_position == 0 or musician.current_position < musician.best_position:
            musician.best_position = musician.current_position
            musician.save()

    return Response({"message": "Points added correctly."})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_points_trophy(request):
    musician_ids = request.data.get("musicianIds")
    points_to_add = request.data.get("pointsToAdd")
    classification = request.data.get("classification")

    if points_to_add == 100:
        typeAward = 3;
    elif points_to_add == 200:
        typeAward = 4;

    if musician_ids and points_to_add:
        
        musicians = Musician.objects.filter(profile=request.user).filter(id__in=musician_ids)
        for musician in musicians:
            musician.points += points_to_add
            musician.points_semester += points_to_add
            musician.points_year += points_to_add
            musician.save()

            award = Award.objects.create(
                type_award=typeAward,
                description=classification,
                points=points_to_add,      
            )
            musician.awards.add(award)


    musiciansr = Musician.objects.filter(profile=request.user)

    musicians_sorted = sorted(musiciansr, key=lambda musician: musician.points, reverse=True)

    for position, musician in enumerate(musicians_sorted, start=1):
        musician.current_position = position
        musician.save()

        if musician.best_position == 0 or musician.current_position < musician.best_position:
            musician.best_position = musician.current_position
            musician.save()

    return Response({"message": "Points and Award added correctly."})


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_points_to_musicians(request):
    musician_ids = request.data.get("musicianIds")
    points_to_add = request.data.get("pointsToAdd")
    classification = request.data.get("classification")

    if musician_ids and points_to_add:
        
        musicians = Musician.objects.filter(id__in=musician_ids)
        for musician in musicians:
            musician.points += points_to_add
            musician.points_semester += points_to_add
            musician.points_year += points_to_add
            musician.save()

            award = Award.objects.create(
                type_award=2,
                description=classification,
                points=points_to_add,    
            )
            musician.awards.add(award)

    musicians = Musician.objects.filter(profile=request.user)

    musicians_sorted = sorted(musicians, key=lambda musician: musician.points, reverse=True)

    for position, musician in enumerate(musicians_sorted, start=1):
        musician.current_position = position
        musician.save()

        if musician.best_position == 0 or musician.current_position < musician.best_position:
            musician.best_position = musician.current_position
            musician.save()

    return Response({"message": "Points and Award added correctly."})