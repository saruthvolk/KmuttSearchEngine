# Generated by Django 3.2.6 on 2022-01-26 15:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionanswer',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 26, 15, 11, 42)),
        ),
        migrations.AlterField(
            model_name='questionanswer',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 26, 15, 11, 42)),
        ),
        migrations.AlterField(
            model_name='questionanswer',
            name='updated_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 26, 15, 11, 42)),
        ),
        migrations.AlterField(
            model_name='questionanswer',
            name='updated_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 26, 15, 11, 42)),
        ),
    ]
