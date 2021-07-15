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


from django.db.models.signals import pre_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json


#  Уведомление об успешном одобреннии заявки
@receiver(pre_save, sender=Participant)
def on_change(sender, instance, **kwargs):
    if instance.id is None: # Add in the participants
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
        f"user_{str(instance.user.pk)}", {
            "type": "user.gossip",
            "event": "Add in the participants",
            "message": f"Ваша заявка по объявлению {instance.ad.title} была успешно одобренна.",
            "participant": {
                "user": {
                    "id": instance.user.pk,
                    "username": instance.user.username,
                    "photo": '/images/' + str(instance.user.photo)
                },
                "information_about_bid": {
                    "number_of_person": instance.number_of_person,
                    "number_of_girls": instance.number_of_girls,
                    "number_of_boys": instance.number_of_boys,
                    "photos": '/images/' + str(instance.photos)
                }
            }
        }
    )
