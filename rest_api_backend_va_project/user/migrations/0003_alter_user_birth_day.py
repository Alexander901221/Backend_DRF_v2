# Generated by Django 3.2 on 2021-07-14 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210714_0531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_day',
            field=models.DateField(null='2021-03-03'),
        ),
    ]
