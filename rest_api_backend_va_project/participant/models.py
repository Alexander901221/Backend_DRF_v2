from django.db import models

from user.models import User
from ad.models import Ad


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Имя")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name="Название объявления")
    number_of_person = models.IntegerField(verbose_name="Количество человек")
    number_of_girls = models.IntegerField(verbose_name="Количество девушек")
    number_of_boys = models.IntegerField(verbose_name="Количество парней")
    photos = models.ImageField(upload_to='images/participants', blank=True)
    create_ad = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
