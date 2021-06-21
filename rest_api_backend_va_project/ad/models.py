from django.db import models

from user.models import User

from utils.choices.choices import CITIES


class Ad(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название объявления")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    city = models.CharField(choices=CITIES, max_length=1, verbose_name="Город")
    geolocation = models.CharField(blank=True, null=True, max_length=100)
    number_of_person = models.IntegerField(verbose_name="Количество человек")
    number_of_girls = models.IntegerField(verbose_name="Количество девушек")
    number_of_boys = models.IntegerField(verbose_name="Количество парней")
    party_date = models.DateTimeField(verbose_name="Дата вечеринки")
    participants = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    create_ad = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title
