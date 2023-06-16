from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class Exercise(models.Model):
    name = models.CharField()
    category = models.IntegerField()
    description = models.CharField()
    url = models.CharField()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_exercises = models.ManyToManyField(Exercise)


class Workout(models.Model):
    date = models.DateField("Workout Date")
    category = ArrayField(models.IntegerField())
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Activity(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)


class Set(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    category = models.IntegerField()
    duration = models.IntegerField(blank=True)
    reps = models.IntegerField(blank=True)
    weight = models.IntegerField(blank=True)
