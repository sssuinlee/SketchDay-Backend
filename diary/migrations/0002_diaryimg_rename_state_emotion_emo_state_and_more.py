# Generated by Django 4.2 on 2023-05-13 16:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("diary", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiaryImg",
            fields=[
                (
                    "diary_img_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("prompt", models.CharField(max_length=1000)),
                ("url", models.TextField()),
                ("thumbnail_url", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name="emotion",
            old_name="state",
            new_name="emo_state",
        ),
        migrations.RenameField(
            model_name="weather",
            old_name="state",
            new_name="wea_state",
        ),
        migrations.RemoveField(
            model_name="emotion",
            name="id",
        ),
        migrations.RemoveField(
            model_name="weather",
            name="id",
        ),
        migrations.AddField(
            model_name="emotion",
            name="emo_id",
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="weather",
            name="wea_id",
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="Diary",
            fields=[
                (
                    "diary_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(default="", max_length=120, null=True)),
                ("content", models.CharField(max_length=255)),
                ("image_url", models.CharField(max_length=200, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "diary_img_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="diary.diaryimg",
                    ),
                ),
                (
                    "emo_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="diary.emotion"
                    ),
                ),
                ("user_id", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                (
                    "wea_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="diary.weather"
                    ),
                ),
            ],
        ),
    ]