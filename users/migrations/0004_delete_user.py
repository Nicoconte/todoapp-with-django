# Generated by Django 3.1.3 on 2020-12-08 00:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
