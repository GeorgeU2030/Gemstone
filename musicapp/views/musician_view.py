from rest_framework import viewsets
from musicapp.serializers import MusicianSerializer, MusicianCreateSerializer, MusicianAwardSerializer
from musicapp.models import Musician


class MusicianView(viewsets.ModelViewSet):
    queryset = Musician.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MusicianCreateSerializer
        return MusicianSerializer
