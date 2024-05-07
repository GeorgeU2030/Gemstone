from django.contrib import admin

# Register your models here.

from .models import User, Award, Musician, Song, Rank, Ranking

admin.site.register(User)
admin.site.register(Award)
admin.site.register(Musician)
admin.site.register(Song)
admin.site.register(Rank)
admin.site.register(Ranking)