from rest_framework import viewsets, status
from musicapp.serializers import AwardSerializer
from musicapp.models import Award, Musician
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response


class AwardView(viewsets.ModelViewSet):
    serializer_class = AwardSerializer
    queryset = Award.objects.all()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def awards_musician(request, musician_id):
    musician = Musician.objects.filter(profile=request.user).get(id=musician_id)
    if not musician:
        return Response({"error": "Musician not found"}, status=status.HTTP_404_NOT_FOUND)
    
    awards = {
        "week": musician.awards.filter(type_award=1).count(),
        "january": musician.awards.filter(description="january").count(),
        "february": musician.awards.filter(description="february").count(),
        "march": musician.awards.filter(description="march").count(),
        "april": musician.awards.filter(description="april").count(),
        "may": musician.awards.filter(description="may").count(),
        "june": musician.awards.filter(description="june").count(),
        "july": musician.awards.filter(description="july").count(),
        "august": musician.awards.filter(description="august").count(),
        "september": musician.awards.filter(description="september").count(),
        "october": musician.awards.filter(description="october").count(),
        "november": musician.awards.filter(description="november").count(),
        "december": musician.awards.filter(description="december").count(),
        "sixmonth": musician.awards.filter(type_award=3).count(),
        "year": musician.awards.filter(type_award=4).count(),
    }

    return Response(awards)
    

