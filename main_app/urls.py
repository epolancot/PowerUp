from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("accounts/signup/", views.signup, name="signup"),
    path("privacy/", views.privacy, name="privacy"),
    path("faq/", views.faq, name="faq"),
    path("profile/", views.profile, name="profile"),
    path("profile/<int:pk>/update", views.UserUpdate.as_view(), name="profile_update"),
    path("accounts/signup/", views.signup, name="signup"),
    path("browse/exercises/", views.browse_exercises, name="browse_exercises"),
    path("browse/workouts/", views.browse_workouts, name="browse_workouts"),
    path(
        "browse/workouts/<int:workout_id>/",
        views.browse_workout_detail,
        name="browse_workout_detail",
    ),
    path("workouts/", views.workouts_index, name="index"),
    path("workouts/dashboard/", views.dashboard, name="dashboard"),
    path("workouts/<int:workout_id>/", views.workouts_detail, name="detail"),
    path(
        "workouts/<int:exercise_id>/favorite/",
        views.favorite_exercise,
        name="favorite_exercise",
    ),
    path(
        "workouts/<int:exercise_id>/unfavorite/",
        views.unfavorite_exercise,
        name="unfavorite_exercise",
    ),
    path("workouts/new/", views.new_workout, name="new_workout"),
    path("workouts/create/", views.create_workout, name="create_workout"),
    path(
        "workouts/<int:workout_id>/delete/", views.delete_workout, name="delete_workout"
    ),
    path("workouts/<int:workout_id>/log/", views.log_workout, name="log_workout"),
    path(
        "workouts/<int:workout_id>/publish/",
        views.publish_workout,
        name="publish_workout",
    ),
    path("workouts/<int:workout_id>/copy/", views.copy_workout, name="copy_workout"),
    path("workouts/<int:workout_id>/search", views.search, name="search"),
    path(
        "workouts/<int:workout_id>/search_favorites",
        views.search_favorites,
        name="search_favorites",
    ),
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
