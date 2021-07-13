from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.choices.choices import CITIES, SEX


class Subscription(models.Model):
    # subscribers = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name='Подписчики')
    # # subscribers = models.ManyToManyField("User", verbose_name="Подписчики")
    author = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name='Подписчик', related_name="author_subscriber")
    date_start = models.DateTimeField(auto_now_add=True, verbose_name="Дата начало подписки")
    date_end = models.DateTimeField(verbose_name="Дата конца подписки")

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class User(AbstractUser):
    city = models.CharField(choices=CITIES, max_length=1)
    birth_day = models.DateField(null='2021-03-03')
    sex = models.CharField(choices=SEX, max_length=100)
    photo = models.ImageField(upload_to='avatar/%Y/%m/%d')
    confirm_email = models.BooleanField(default=False)
    confirm_account = models.BooleanField(default=False)
    code_confirm = models.IntegerField(null=True, blank=True, unique=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, verbose_name='Подписка', null=True)

    class Meta:
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name


from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


#  Уведомление о создание и изменения пользователя
@receiver(pre_save, sender=User)
def on_change(sender, instance: User, **kwargs):
    print('instance -> ', instance)  # User который изменяет свои данные
    print('sender -> ', sender)

    if instance.id is None: # создание нового user
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{str(instance.pk)}", {
                "type": "user.gossip",
                "event": "New User",
                "username": instance.username
            }
        )
    else:
        previous = User.objects.get(id=instance.id)
        if previous.confirm_account != instance.confirm_account: # поле было измененно
            if instance.confirm_account:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"user_{str(instance.pk)}", {
                        "type": "user.gossip",
                        "event": "Success confirm account",
                        "username": instance.username,
                        "message": "Ваш аккаунт успешно подтвержден"
                    }
                )
            else:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"user_{str(instance.pk)}", {
                        "type": "user.gossip",
                        "event": "Error confirm account",
                        "username": instance.username,
                        "message": "Ваш аккаунт не подтвержден"
                    }
                )


# #  Уведомление о удаление пользователя
# @receiver(pre_delete, sender=User)
# def announce_new_user2(sender, instance, **kwargs):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         f"user_{str(instance.pk)}", {
#             "type": "user.gossip",
#             "event": "Delete User",
#             "username": instance.username
#         }
#     )
