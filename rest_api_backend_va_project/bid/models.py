from django.db import models
from user.models import User
from ad.models import Ad


class Bid(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name="Название объявления")
    number_of_person = models.IntegerField(verbose_name="Количество человек")
    number_of_girls = models.IntegerField(verbose_name="Количество девушек")
    number_of_boys = models.IntegerField(verbose_name="Количество парней")
    photos = models.ImageField(upload_to='bids/%Y/%m/%d')
    create_ad = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.pk}'


from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from .consumers import BidConsumer


#  Уведомление о создание и изменения объявления
@receiver(pre_save, sender=Bid)
def on_change(sender, instance, **kwargs):

    if instance.id is None: # Create a new ad
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"ad_{str(instance.ad.pk)}", {
                "type": "bid",
                "event": "Create bid",
                "bid": {
                    "author-bid": {
                        "id": instance.author.pk,
                        "username": instance.author.username,
                        "photo": '/images/' + str(instance.author.photo)
                    },
                    "data": {
                        "number_of_person": instance.number_of_person,
                        "number_of_girls": instance.number_of_girls,
                        "number_of_boys": instance.number_of_boys,
                        "photos": '/images/' + str(instance.photos)
                    }
                },
                "ad": {
                    "id_ad": instance.ad.pk,
                    "author-ad": {
                        "id": instance.ad.author.pk,
                        "username": instance.ad.author.username
                    }
                }
            }
        )
