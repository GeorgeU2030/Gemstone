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
        "january": musician.awards.filter(description="January").count(),
        "february": musician.awards.filter(description="February").count(),
        "march": musician.awards.filter(description="March").count(),
        "april": musician.awards.filter(description="April").count(),
        "may": musician.awards.filter(description="May").count(),
        "june": musician.awards.filter(description="June").count(),
        "july": musician.awards.filter(description="July").count(),
        "august": musician.awards.filter(description="August").count(),
        "september": musician.awards.filter(description="September").count(),
        "october": musician.awards.filter(description="October").count(),
        "november": musician.awards.filter(description="November").count(),
        "december": musician.awards.filter(description="December").count(),
        "sixmonth": musician.awards.filter(type_award=3).count(),
        "year": musician.awards.filter(type_award=4).count(),
    }

    return Response(awards)
    

