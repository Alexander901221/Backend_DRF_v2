from django.db import models

from user.models import User

from utils.choices.choices import CITIES


class MyManager(models.Manager):
    def custom_filter(self, **kwargs):
        kwargs['is_published'] = True
        return super().get_queryset().filter(**kwargs)

    def custom_order_by(self, *args):
        args = ('party_date',) + args
        return super().get_queryset().order_by(*args)


class Ad(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название объявления")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    city = models.CharField(choices=CITIES, max_length=1, verbose_name="Город")
    geolocation = models.CharField(blank=True, null=True, max_length=100)
    number_of_person = models.IntegerField(verbose_name="Количество человек")
    number_of_girls = models.IntegerField(verbose_name="Количество девушек")
    number_of_boys = models.IntegerField(verbose_name="Количество парней")
    party_date = models.DateTimeField(verbose_name="Дата вечеринки")
    # participants = models.IntegerField(default=0)
    participants = models.ManyToManyField(User, verbose_name="Участники", related_name="participant_users")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    create_ad = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title

    objects = models.Manager()
    custom_manager = MyManager()


from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json

def to_json(obj):
    return {
        'id': obj.pk,
        'photo': '/images/' + str(obj.photo)
    }

#  Уведомление о создание и изменения объявления
@receiver(pre_save, sender=Ad)
def on_change(sender, instance, **kwargs):

    if instance.id is None: # Create a new ad
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_id_{instance.author.pk}", {
                "type": "ad",
                "event": "Create ad",
                "username": instance.author.username,
                "ad_title": instance.title
            }
        )
    else:
        previous = Ad.objects.get(id=instance.id)
        participant = []
        for element in previous.participants.all():
            result = to_json(element)
            participant.append(result)
        
        if previous.is_published != instance.is_published: # check on change field
            if instance.is_published:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"city_{instance.city}", {
                        "type": "ad",
                        "event": "Ad published",
                        "message": "Объявление было успешно опубликованно",
                        "geolocation": previous.geolocation,
                        "id_ad": previous.pk,
                        "ad": {
                            "id": previous.pk,
                            "title": previous.title,
                            "author": {
                                "id": previous.author.pk,
                                "photo": '/images/' + str(previous.author.photo)
                            },                        
                            "number_of_person": previous.number_of_person,
                            "number_of_girls": previous.number_of_girls,
                            "number_of_boys": previous.number_of_boys,
                            "party_date": json.dumps(previous.party_date, indent=4, sort_keys=True, default=str),
                            "participants": participant,
                        }
                    }
                )
