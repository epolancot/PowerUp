from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import requests


class Exercise(models.Model):
    name = models.CharField()
    wger_id = models.IntegerField()
    category = models.IntegerField()
    description = models.CharField()

    @classmethod
    def check_new_exercise(cls, exercise_id):
        existing_exercise = Exercise.objects.filter(wger_id=exercise_id)
        if not existing_exercise:
            response = requests.get(f"https://wger.de/api/v2/exercise/{exercise_id}/")
            exercise = response.json()
            new_exercise = Exercise.objects.create(
                name=exercise["name"],
                wger_id=exercise["id"],
                category=exercise["category"],
                description=exercise["description"],
            )
            new_exercise.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_exercises = models.ManyToManyField(Exercise)

    def username(self):
        user = self.user
        return f"{self.user.username}"


class Workout(models.Model):
    date = models.DateField("Workout Date")
    category = ArrayField(models.IntegerField())
    category_text = ArrayField(models.CharField())
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    logged = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("detail", kwargs={"workout_id": self.id})

    def display_categories(self):
        return ", ".join(self.category_text)

    class Meta:
        ordering = ["-date"]


class Activity(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    category = models.IntegerField()
    name = models.CharField()
    description = models.CharField()


class Set(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    duration = models.IntegerField(blank=True)
    reps = models.IntegerField(blank=True)
    weight = models.IntegerField(blank=True)
