# Generated by Django 4.2.1 on 2023-08-19 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("samplesapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="samplesmodel",
            name="species",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]