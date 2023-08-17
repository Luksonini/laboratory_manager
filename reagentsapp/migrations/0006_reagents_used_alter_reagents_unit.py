# Generated by Django 4.2.1 on 2023-08-17 21:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reagentsapp", "0005_alter_reagents_unit"),
    ]

    operations = [
        migrations.AddField(
            model_name="reagents",
            name="used",
            field=models.FloatField(
                default=0, validators=[django.core.validators.MinValueValidator(0)]
            ),
        ),
        migrations.AlterField(
            model_name="reagents",
            name="unit",
            field=models.CharField(
                choices=[
                    ("-", "-"),
                    ("ml", "ml"),
                    ("ul", "ul"),
                    ("g", "g"),
                    ("mg", "mg"),
                    ("szt", "sztuk"),
                ],
                default="ml",
                max_length=5,
            ),
        ),
    ]
