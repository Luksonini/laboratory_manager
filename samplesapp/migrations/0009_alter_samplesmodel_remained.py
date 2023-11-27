# Generated by Django 4.2.4 on 2023-11-09 14:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("samplesapp", "0008_alter_samplesmodel_remained"),
    ]

    operations = [
        migrations.AlterField(
            model_name="samplesmodel",
            name="remained",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
    ]