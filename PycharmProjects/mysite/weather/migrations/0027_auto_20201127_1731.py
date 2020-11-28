# Generated by Django 3.1.3 on 2020-11-27 15:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0026_auto_20201127_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='date',
        ),
        migrations.AddField(
            model_name='cityweather',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 27, 15, 31, 14, 60399, tzinfo=utc), verbose_name='date requested'),
        ),
        migrations.AlterField(
            model_name='historyreq',
            name='date_to',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 27, 15, 31, 14, 60399, tzinfo=utc)),
        ),
    ]
