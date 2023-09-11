# Generated by Django 4.2.1 on 2023-08-19 17:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SamplesModel",
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
                ("sample_date", models.DateField(auto_now_add=True)),
                ("sample_name", models.CharField(max_length=200)),
                ("owner", models.CharField(blank=True, max_length=200, null=True)),
                ("location", models.CharField(max_length=200)),
                (
                    "quantity",
                    models.FloatField(
                        default=0,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "sample_type",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                (
                    "access_key",
                    models.CharField(blank=True, max_length=32, unique=True),
                ),
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
    ]