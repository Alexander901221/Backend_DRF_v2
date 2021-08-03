# Generated by Django 3.2 on 2021-08-03 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipantImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_participants', models.ImageField(upload_to='participant/photo_participants/%Y/%m/%d', verbose_name='Фото участников')),
                ('photo_alcohol', models.ImageField(upload_to='participant/photo_alcohol/%Y/%m/%d', verbose_name='Фото алкоголя')),
            ],
            options={
                'verbose_name': 'Фотография',
                'verbose_name_plural': 'Фотографии',
            },
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_person', models.IntegerField(verbose_name='Количество человек')),
                ('number_of_girls', models.IntegerField(verbose_name='Количество девушек')),
                ('number_of_boys', models.IntegerField(verbose_name='Количество парней')),
                ('create_ad', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ad.ad', verbose_name='Название объявления')),
                ('photos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='participant.participantimages', verbose_name='Фотографии')),
            ],
            options={
                'verbose_name': 'Участник',
                'verbose_name_plural': 'Участники',
            },
        ),
    ]
