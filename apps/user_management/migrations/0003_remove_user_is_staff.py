# Generated by Django 5.0.1 on 2024-01-31 06:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("user_management", "0002_user_is_staff"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="is_staff",
        ),
    ]