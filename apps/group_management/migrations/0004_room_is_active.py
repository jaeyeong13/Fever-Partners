# Generated by Django 5.0.1 on 2024-02-03 00:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("group_management", "0003_room_favor_offline"),
    ]

    operations = [
        migrations.AddField(
            model_name="room",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]
