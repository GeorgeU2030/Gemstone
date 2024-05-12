from rest_framework import viewsets
from musicapp.serializers import MusicianSerializer, MusicianCreateSerializer, MusicianAwardSerializer
from musicapp.models import Musician
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.db.models import Count


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


