from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("accounts/signup/", views.signup, name="signup"),
    path("workouts/", views.workouts_index, name="index"),
    path("workouts/dashboard/", views.dashboard, name="dashboard"),
    path("workouts/<int:workout_id>/", views.workouts_detail, name="detail"),
    path("workouts/new/", views.new_workout, name="new_workout"),
    path("workouts/create/", views.create_workout, name="create_workout"),
    path("workouts/<int:workout_id>/log/", views.log_workout, name="log_workout"),
    path("workouts/<int:workout_id>/copy/", views.copy_workout, name="copy_workout"),
    path("workouts/<int:workout_id>/search", views.search, name="search"),
    path(
        "workouts/<int:workout_id>/create_activity/<int:exercise_id>/",
        views.create_activity,
        name="create_activity",
    ),
    path(
        "workouts/<int:workout_id>/delete_activity/<int:activity_id>/",
        views.delete_activity,
        name="delete_activity",
    ),
    path(
        "workouts/<int:workout_id>/create_set/<int:activity_id>/",
        views.create_set,
        name="create_set",
    ),
    path(
        "workouts/<int:workout_id>/delete_set/<int:set_id>/",
        views.delete_set,
        name="delete_set",
    ),
]
