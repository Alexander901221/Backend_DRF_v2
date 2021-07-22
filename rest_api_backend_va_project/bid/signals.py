import json
from django.db.models.signals import pre_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .consumers import BidConsumer
from .models import Bid


#  Уведомление о создание и изменения заявки
@receiver(pre_save, sender=Bid)
def on_change(sender, instance, **kwargs):

    if instance.id is None: # Create a new bid
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
                        "photos": {
                            "photo_participants": '/images/' + str(instance.photos.photo_participants),
                            "photo_alcohol": '/images/' + str(instance.photos.photo_alcohol),
                        }
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
