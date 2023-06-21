from django.shortcuts import render, redirect
from .models import Profile, Workout, Activity, Exercise, User, Set
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from fuzzywuzzy import fuzz
from collections import Counter
import datetime
import random

# Create your views here.

categories = {
    8: "Arms",
    10: "Abs",
    12: "Back",
    14: "Calves",
    11: "Chest",
    9: "Legs",
    13: "Shoulders",
    15: "Cardio",
}


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
def profile(request):
    return render(request, "profile/index.html", {"user": request.user})


class UserUpdate(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    success_url = "/profile"


@login_required
def about(request):
    return render(request, "about.html", {"title": "About"})


@login_required
def workouts_index(request):
    workouts = Workout.objects.filter(profile=Profile.objects.get(user=request.user))
    return render(
        request, "workouts/index.html", {"workouts": workouts, "title": "Home"}
    )


@login_required
def workouts_detail(request, workout_id):
    workout = Workout.objects.get(id=workout_id)

    if request.method == "POST":
        target = request.POST[""]
    return render(
        request, "workouts/detail.html", {"title": "Workout", "workout": workout}
    )


@login_required
def new_workout(request):
    return render(request, "main_app/workout_form.html", {"title": "New Workout"})


@login_required
def create_workout(request):
    category = [int(i) for i in request.POST["category"].split(",")]
    category_text = [categories[cat] for cat in category]
    if request.POST["date"]:
        date = request.POST["date"]
    else:
        date = datetime.date.today()
    new_workout = Workout.objects.create(
        profile=Profile.objects.get(user=request.user),
        date=date,
        category=category,
        category_text=category_text,
    )
    new_workout.save()
    return redirect("detail", workout_id=new_workout.id)


@login_required
def log_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    workout.logged = True
    return redirect("detail", workout_id=workout.id)


@login_required
def publish_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    if workout.logged == True:
        workout.published = True
    return redirect("detail", workout_id=workout.id)


@login_required
def copy_workout(request, workout_id):
    workout = Workout.objects.get(id=workout_id)
    print
    activities = Activity.objects.filter(workout=workout)
    new_workout = Workout.objects.create(
        profile=request.user,
        date=datetime.date.today(),
        category=workout.category,
    )
    new_workout.save()
    print(activities)
    for activity in activities:
        exercise = activity.exercise
        new_activity = Activity.objects.create(
            exercise=exercise,
            workout=new_workout,
            category=exercise.category,
            name=exercise_object.name,
            description=exercise_object.description,
        )
        new_activity.save()
    return redirect("detail", workout_id=new_workout.id)


@login_required
def create_activity(request, workout_id, exercise_id):
    Exercise.check_new_exercise(exercise_id)
    exercise_object = Exercise.objects.get(wger_id=exercise_id)
    new_activity = Activity.objects.create(
        exercise=exercise_object,
        workout=Workout.objects.get(id=workout_id),
        category=exercise_object.category,
        name=exercise_object.name,
        description=exercise_object.description,
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
    new_set = Set.objects.create(
        activity=activity,
        duration=request.POST["duration"],
        reps=request.POST["reps"],
        weight=request.POST["weight"],
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
    sorted_results = []
    error_message = ""
    for category in workout.category:
        response = requests.get(
            f"https://wger.de/api/v2/exercise/?category={category}&language=2&limit=160"
        )
        category_exercises = response.json()
        relevant_exercises.extend(category_exercises["results"])
    if request.method == "POST":
        target = request.POST["search"]
        sorted_results = sorted(
            relevant_exercises,
            key=lambda x: fuzz.token_sort_ratio(x["name"], target),
            reverse=True,
        )
        if len(sorted_results) > 0:
            error_message = "No results match your search."
    results_filter = [
        activity.exercise.wger_id for activity in workout.activity_set.all()
    ]
    for result in sorted_results[:5]:
        results_filter.append(result["id"])
    filtered_results = list(
        filter(lambda x: x["id"] not in results_filter, relevant_exercises)
    )
    suggested_exercises = random.sample(filtered_results, 10)

    return render(
        request,
        "workouts/search.html",
        {
            "workout_id": workout_id,
            "suggested_exercises": suggested_exercises,
            "search_results": sorted_results[:5],
            "error_message": error_message,
        },
    )


@login_required
def dashboard(request):
    # focus distribution
    all_workouts = Workout.objects.filter(user=request.user)
    category_list = []
    for workout in all_workouts:
        focus_distribution.extend(workout.category)
    category_frequency = Counter(category_list)
    print(category_frequency)

    # workout frequency
    today = datetime.date.today()
    signup_date = request.user.date_joined.date()
    days_since_signup = (today - signup_date).days
    workout_frequency = days_since_signup / length(all_workouts)
    print(workout_frequency)

    # top exercises
    workout_ids = [workout.id for workout in all_workouts]
    activity_list = Activity.objects.filter(workout__in=workout_ids)
    exercise_list = [activity.exercise.id for exercise in activity_list]
    top_exercises = sorted(
        Counter(exercise_list).items(), key=lambda x: x[1], reverse=True
    )
    print(top_exercises)

    # current streak
    workout_streak = 0
    workout_message = ""
    previous_workout_dates = [workout.date for workout in all_workouts]
    while True:
        check_date = today - datetime.timedelta(days=1 + workout_streak)
        if check_date not in previous_workout_dates:
            break
        workout_streak += 1
    if today in previous_workout_dates:
        workout_streak += 1
        workout_message = (
            "Great job! exercise again tomorrow to keep building your streak"
        )
    else:
        if workout_streak == 0:
            workout_message = "Log a workout today and start building your streak!"
        else:
            workout_message = "Log a workout for today and keep building your streak!"
    print(workout_streak, workout_message)

    return render(
        request,
        "workouts/dashboard.html",
        {
            "category_frequency": category_frequency,
            "workout_frequency": workout_frequency,
            "top_exercises": top_exercises,
            "workout_workout_streak": workout_streak,
            "workout_message": workout_message,
        },
    )


@login_required
def favorite_exercise(request, exercise_id):
    Exercise.check_new_exercise(exercise_id)
    exercise_object = Exercise.objects.get(wger_id=exercise_id)
    Profile.objects.get(user=request.user).favorite_exercises.add(exercise_object.id)
    return redirect("browse_exercises")


@login_required
def unfavorite_exercise(request, exercise_id):
    exercise_object = Exercise.objects.get(wger_id=exercise_id)
    Profile.objects.get(user=request.user).favorite_exercises.remove(exercise_object.id)
    return redirect("browse_exercises")


@login_required
def browse_exercises(request):
    results = []
    sorted_results = []
    if request.method == "POST":
        category = request.POST.get("category")
        if category:
            response = requests.get(
                f"https://wger.de/api/v2/exercise/?category={category}&language=2&limit=160"
            )
            category_exercises = response.json()
            results.extend(category_exercises["results"])
        else:
            response = requests.get(
                f"https://wger.de/api/v2/exercise/?language=2&limit=385"
            )
            category_exercises = response.json()
            results.extend(category_exercises["results"])
        target = request.POST["search"]
        sorted_results = sorted(
            results,
            key=lambda x: fuzz.token_sort_ratio(x["name"], target),
            reverse=True,
        )
    profile = Profile.objects.get(user=request.user)
    favorite_exercises = [
        exercise.wger_id for exercise in profile.favorite_exercises.all()
    ]
    return render(
        request,
        "browse/exercises.html",
        {
            "search_results": sorted_results[:10],
            "favorite_exercises": favorite_exercises,
        },
    )


@login_required
def browse_workouts(request):
    available_workouts = Workout.objects.filter(published=True).exclude(
        profile=Profile.objects.get(user=request.user)
    )
    sorted_results = []
    category = request.POST.get("category")
    if category:
        available_workouts = list(
            filter(lambda x: category in x["category"], available_workouts)
        )
    target = request.POST["search"]
    sorted_results = sorted(
        available_workouts,
        key=lambda x: fuzz.token_sort_ratio(x.profile.username(), target),
        reverse=True,
    )
    return render(
        request, "browse/workouts.html", {"search_results": sorted_results[:10]}
    )
