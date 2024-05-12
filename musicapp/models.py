from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.TextField()

    def __str__(self):
        return f"{self.username} - {self.email}"


class Award(models.Model):
    description = models.TextField()
    # 1 - Song
    # 2 - Month
    # 3 - Semester
    # 4 - Year
    type_award = models.IntegerField()

    def __str__(self):
        return f"{self.description}"


class Musician(models.Model):
    name = models.CharField(max_length=100)
    photo = models.TextField()
    flag = models.TextField()
    country = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    best_position = models.IntegerField(default=0)
    current_position = models.IntegerField(default=0)
    start_date_best_position = models.DateField(null=True)
    end_date_best_position = models.DateField(null=True)
    points_year = models.IntegerField(default=0)
    points_semester = models.IntegerField(default=0)
    awards = models.ManyToManyField(Award, related_name="musicians", blank=True)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.country}"


class Song(models.Model):
    name = models.CharField(max_length=100)
    gem = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    week = models.IntegerField(default=0)
    release_year = models.PositiveSmallIntegerField()
    genre = models.CharField(max_length=100)
    album = models.TextField()
    youtube = models.TextField()
    musicians = models.ManyToManyField(Musician, related_name="songs")
    profile = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Rank(models.Model):
    week = models.IntegerField()
    position = models.IntegerField()
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.week}"


class Ranking(models.Model):
    period = models.CharField(max_length=50)
    points = models.IntegerField()
    musician = models.ForeignKey(Musician, on_delete=models.CASCADE)

    def __str__(self):
        return f"Ranking {self.period}"
