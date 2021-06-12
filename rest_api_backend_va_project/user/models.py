from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.choices.choices import CITIES, SEX


class User(AbstractUser):
    city = models.CharField(choices=CITIES, max_length=1)
    birth_day = models.DateField(null='2021-03-03')
    sex = models.CharField(choices=SEX, max_length=100)
    photo = models.ImageField(upload_to='avatar/%Y/%m/%d')
    confirm_email = models.BooleanField(default=False)
    confirm_account = models.BooleanField(default=False)
    code_confirm = models.IntegerField(null=True, blank=True, unique=True)

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name
