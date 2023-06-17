from django.shortcuts import render, redirect
from .models import Profile, Workout, Activity, Exercise
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests

# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid sign up - try again"
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)


@login_required
def about(request):
    return render(request, "about.html")


@login_required
def workouts_index(request):
    return render(request, "workouts/index.html")


@login_required
def workouts_detail(request, workout_id):
    workouts = Workout.objects.get(id=workout_id)
    return render(request, "workouts/detail.html")


@login_required
def new_workout(request):
    return render(request, "main_app/workout_form.html")


@login_required
def workout_create(request):
    new_workout = Workout.objects.create(
        date=request.POST.date, category=request.POST.category
    )
    new_workout.save()
    return redirect("detail", workout_id=new_workout.id)


@login_required
def activity_create(request, workout_id, exercise_id):
    Exercise.check_new_exercise(exercise_id)
    exercise_object = exercise.objects.get(wger_id=exercise_id)
    new_activity = Activity.objects.create(
        exercise=exercise_object.id, workout=workout_id
    )
    new_activity.save()
    return redirect("detail", workout_id=workout_id)
