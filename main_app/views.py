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
def create_workout(request):
    category = [int(i) for i in request.POST["category"].split(",")]
    new_workout = Workout.objects.create(
        user=request.user.id,
        date=request.POST["date"],
        category=category,
    )
    new_workout.save()
    return redirect("detail", workout_id=new_workout.id)


@login_required
def create_activity(request, workout_id, exercise_id):
    Exercise.check_new_exercise(exercise_id)
    exercise_object = exercise.objects.get(wger_id=exercise_id)
    new_activity = Activity.objects.create(
        exercise=exercise_object.id,
        workout=workout_id,
        category=exercise_object.category,
    )
    new_activity.save()
    return redirect("detail", workout_id=workout_id)


@login_required
def delete_activity(request, workout_id, activity_id):
    activity = Activity.objects.get(id=activity_id)
    activity.delete()
    return redirect("detail", workout_id=workout_id)


@login_required
def create_set(request, workout_id, activity_id):
    activity = Activity.objects.get(id=activity_id)
    if activity.category == 15:
        new_set = Set.objects.create(
            activity=activity_id, duration=request.POST.duration
        )
    else:
        new_set = Set.objects.create(
            activity=activity_id, reps=request.POST.reps, weight=request.POST.weight
        )
    new_set.save()
    return redirect("detail", workout_id=workout_id)


@login_required
def delete_set(request, workout_id, set_id):
    set_record = Set.objects.get(id=set_id)
    set_record.delete()
    return redirect("detail", workout_id=workout_id)


@login_required
def search(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    relevant_exercises = []
    search_results = []
    error_message = ""
    for category in workout.category:
        response = requests.get(
            f"https://wger.de/api/v2/exercise/?category={category}&language=2&limit=160"
        )
        category_exercises = response.json()
        relevant_exercises.extend(category_exercises.results)
    if request.method == "POST":
        keywords = request.POST.search.split(" ")
        search_results = filter(
            lambda x: any([word in x for word in keywords]), relevant_exercises
        )
        if length(search_results) > 0:
            error_message = "No results match your search."
    return render(
        request,
        "workouts/search.html",
        {
            "relevant_exercises": relevant_exercises,
            "search_results": search_results,
            "error_message": error_message,
        },
    )
