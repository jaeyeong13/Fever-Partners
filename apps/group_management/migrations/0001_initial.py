# Generated by Django 5.0.1 on 2024-02-02 09:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goal_management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('detail', models.TextField()),
                ('cert_required', models.BooleanField(default=False)),
                ('cert_detail', models.TextField()),
                ('penalty_value', models.PositiveIntegerField(default=0)),
                ('activityTags', models.ManyToManyField(default=None, to='goal_management.activitytag')),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='master', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(default=None, related_name='members', to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(default=None, to='goal_management.tag')),
            ],
        ),
    ]