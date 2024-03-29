# Generated by Django 5.0.1 on 2024-02-11 02:49

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Authentication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "start",
                    models.TimeField(default=datetime.time(0, 0), verbose_name="인증시작"),
                ),
                (
                    "end",
                    models.TimeField(default=datetime.time(2, 0), verbose_name="인증종료"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MemberAuthentication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_auth", models.BooleanField(default=False)),
                (
                    "content",
                    models.CharField(max_length=100, null=True, verbose_name="인증내용"),
                ),
                (
                    "image",
                    models.ImageField(
                        null=True,
                        upload_to="authentication_images/",
                        verbose_name="인증사진",
                    ),
                ),
                ("is_completed", models.BooleanField(default=False)),
                (
                    "created_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
            ],
        ),
    ]
