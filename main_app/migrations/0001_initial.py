# Generated by Django 4.2.2 on 2023-06-21 20:50

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.IntegerField()),
                ('name', models.CharField()),
                ('description', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
                ('wger_id', models.IntegerField()),
                ('category', models.IntegerField()),
                ('description', models.CharField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite_exercises', models.ManyToManyField(to='main_app.exercise')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Workout Date')),
                ('category', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), size=None)),
                ('category_text', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None)),
                ('logged', models.BooleanField(default=False)),
                ('published', models.BooleanField(default=False)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Set',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField(blank=True)),
                ('reps', models.IntegerField(blank=True)),
                ('weight', models.IntegerField(blank=True)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.activity')),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.exercise'),
        ),
        migrations.AddField(
            model_name='activity',
            name='workout',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.workout'),
        ),
    ]
