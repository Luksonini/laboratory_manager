# Generated by Django 4.2.4 on 2023-11-20 12:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("samplesapp", "0008_alter_samplesmodel_remained"),
    ]

    operations = [
        migrations.AlterField(
            model_name="samplesmodel",
            name="sample_date",
            field=models.DateField(),
        ),
    ]
