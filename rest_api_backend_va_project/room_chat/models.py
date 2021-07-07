from django.db import models
from user.models import User
from ad.models import Ad


class Room(models.Model):
    """Модель комнаты чата"""
    ad = models.ForeignKey(Ad, verbose_name="Объявление", on_delete=models.CASCADE)
    invited = models.ManyToManyField(User, verbose_name="Участники", related_name="invited_user")

    class Meta:
        verbose_name = "Комната чата"
        verbose_name_plural = "Комнаты чатов"


class Chat(models.Model):
    """Модель чата"""
    room = models.ForeignKey(Room, verbose_name="Комната чата", on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=500)
    date = models.DateTimeField("Дата отправки", auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чатов"
        ordering = ['-date']

    def __str__(self):
        return self.text
