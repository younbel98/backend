# Generated by Django 5.0.6 on 2025-03-09 08:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_alter_child_day_of_birth_alter_family_day_of_birth_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="child",
            name="day_of_birth",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
