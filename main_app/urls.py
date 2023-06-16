from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("accounts/signup/", views.signup, name="signup"),
    path("workouts/", views.workouts_index, name="index"),
    path("workouts/<int:workout_id>/", views.workouts_detail, name="detail"),
    path("workouts/new/", views.new_workout, name="new_workout"),
    path("workouts/create/", views.workout_create, name="workout_create"),
]
