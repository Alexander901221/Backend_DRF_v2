# Generated by Django 3.2 on 2021-08-03 15:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_last_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_activity',
            field=models.DateTimeField(default=datetime.datetime(2021, 8, 3, 15, 31, 52, 362953, tzinfo=utc), verbose_name='Последний раз в сети'),
        ),
    ]
