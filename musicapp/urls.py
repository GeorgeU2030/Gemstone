from django.urls import path, include
from rest_framework import routers
from musicapp.views import award_view, song_view, musician_view

router = routers.DefaultRouter()
router.register(r"awards", award_view.AwardView, 'awards')
router.register(r"songs", song_view.SongView, 'songs')
router.register(r"musicians", musician_view.MusicianView, 'musicians')

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("get-id-user/", musician_view.get_id_user, name="get-id-user"),
    path("top-musicians-points/", musician_view.top_musicians_points, name="top-musicians-points"),
    path("top-musicians-awards/", musician_view.top_musicians_awards, name="top-musicians-awards"),
    path("ranking/", musician_view.ranking, name="ranking"),
    path("latest-song/", song_view.latest_song, name="latest-song"),
    path("all_songs", song_view.get_all_songs, name="all_songs"),
    path("search_musician/", musician_view.search_musician, name="search_musician"),
    path("last_week/", song_view.last_week, name="last_week"),
    path("update_musicians/", song_view.update_musicians, name="update_musicians"),
    path("song/<int:song_id>",song_view.get_song_by_id, name="song"),
    path("ranking_awards/", musician_view.ranking_awards, name="ranking_awards"),
    path("get_musician/<int:musician_id>", musician_view.get_musician, name="get_musician"),
    path("get_song_musician/<int:musician_id>", song_view.get_songs_by_musician, name="get_song_musician"),
    path("get_awards_musician/<int:musician_id>", award_view.awards_musician, name="get_awards_musician"),
    path("all_musicians/", musician_view.all_musicians, name="all_musicians"),
    path("add_points_week/", musician_view.add_points_week, name="add_points_week"),
    path("add_points_trophy/", musician_view.add_points_trophy, name="add_points_trophy"),
    path("add_points_to_musicians/", musician_view.add_points_to_musicians, name="add_points_to_musicians"),
    
]
