# Generated by Django 3.2.4 on 2021-07-01 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ad', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_person', models.IntegerField(verbose_name='Количество человек')),
                ('number_of_girls', models.IntegerField(verbose_name='Количество девушек')),
                ('number_of_boys', models.IntegerField(verbose_name='Количество парней')),
                ('photos', models.ImageField(blank=True, upload_to='images/bids')),
                ('create_ad', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ad.ad', verbose_name='Название объявления')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
            },
        ),
    ]