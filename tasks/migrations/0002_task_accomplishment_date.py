# Generated by Django 3.1 on 2020-12-10 13:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='accomplishment_date',
            field=models.DateField(default=datetime.date(2020, 12, 10)),
        ),
    ]
