from rest_framework import viewsets
from musicapp.serializers import AwardSerializer
from musicapp.models import Award


class AwardView(viewsets.ModelViewSet):
    serializer_class = AwardSerializer
    queryset = Award.objects.all()

