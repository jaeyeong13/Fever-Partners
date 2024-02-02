# Generated by Django 5.0.1 on 2024-02-01 23:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rooms", "0003_alter_room_master"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="room",
            name="master",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rooms_managed",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
