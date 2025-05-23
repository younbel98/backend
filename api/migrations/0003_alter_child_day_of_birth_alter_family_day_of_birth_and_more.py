# Generated by Django 5.0.6 on 2025-03-09 08:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_encryptionkey"),
    ]

    operations = [
        migrations.AlterField(
            model_name="child",
            name="day_of_birth",
            field=models.DateField(
                default=datetime.datetime(
                    2025, 3, 9, 8, 21, 8, 49477, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="family",
            name="day_of_birth",
            field=models.DateField(default=datetime.date(2025, 3, 9)),
        ),
        migrations.AlterField(
            model_name="personincustody",
            name="day_of_birth",
            field=models.DateField(default=datetime.date(2025, 3, 9)),
        ),
        migrations.AlterField(
            model_name="spouce",
            name="day_of_birth",
            field=models.DateField(default=datetime.date(2025, 3, 9)),
        ),
    ]
