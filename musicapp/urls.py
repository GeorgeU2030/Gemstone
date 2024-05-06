from django.urls import path, include
from rest_framework import routers
from musicapp.views import award_view, song_view, musician_view

router = routers.DefaultRouter()
router.register(r"awards", award_view.AwardView, 'awards')
router.register(r"songs", song_view.SongView, 'songs')
router.register(r"musicians", musician_view.MusicianView, 'musicians')

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
