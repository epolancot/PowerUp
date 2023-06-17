from django.contrib import admin
from .models import Profile, Exercise, Workout, Activity, Set

# Register your models here.
admin.site.register(Profile)
admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(Activity)
admin.site.register(Set)
