from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse

from .serializers import ParticipantSerializer
from ad.models import Ad

from bid.models import Bid
from user.models import User

# Добавление в комнату
from participant.models import Participant


# Получение всех participants (GET)
class ParticipantListView(generics.ListAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = []
    queryset = Participant.objects.all()


# Получение participant по param (GET)
class ParticipantRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = []
    queryset = Participant.objects.all()


# Создание participant (post)
# class ParticipantCreateView(generics.CreateAPIView):
#     serializer_class = ParticipantSerializer
#     permission_classes = []
#     queryset = Participant.objects.all()
#
#     def perform_create(self, serializer):
#         id_ad = self.request.data['id_ad']
#         ad = Ad.objects.get(pk=id_ad)
#         participant = Participant.objects.filter(user=self.request.user, ad=ad)
#         if participant:
#             raise ValidationError('Данный пользователь уже есть у вас в участниках')
#         if ad:
#             serializer.save(user=self.request.user, ad=ad)
#         else:
#             raise ValidationError('Вы уже подали заявку. Дождитесь ответа')


# Получение моих участников
class MyParticipantsListAPIView(generics.ListAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = []

    def get_queryset(self):
        return Participant.objects.filter(ad__author=self.request.user)


# добавление участника
class ParticipantCreateView(generics.CreateAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = []
    queryset = Participant.objects.all()

    def perform_create(self, serializer):
        user_id = self.request.data['user_id']  # id пользователя заявки
        my_ad = Ad.objects.get(author=self.request.user)  # проверка на существования объявления
        participant = Participant.objects.filter(user__pk=user_id)
        if participant:
            raise ValidationError('Данный пользователь уже находится в вашем списке участников')
        if my_ad:
            user = User.objects.get(pk=user_id)
            check_user_bid = Bid.objects.filter(author__pk=user_id, ad__author=self.request.user)
            if check_user_bid:
                check_user_bid.delete()
                serializer.save(user=user, ad=my_ad)
                # Количество участников добавляется в поле participant в объявлении
                count_participant = Participant.objects.filter(ad=my_ad).count()
                my_ad.participants = int(count_participant)
                my_ad.save()
                # Добавление в комнату чата
                #
                #
            else:
                raise ValidationError('Данного user нет в ваших заявках')
        else:
            raise ValidationError('У вас не созданно объявление')


# Удаление участника
class ParticipantDestroyAPIView(generics.DestroyAPIView):
    serializer_class = ParticipantSerializer
    permission_classes = []
    queryset = Participant.objects.all()

    def delete(self, request, *args, **kwargs):
        param = kwargs['pk']
        user = self.request.user
        ad_author = Participant.objects.filter(ad__author=user)
        my_ad = Ad.objects.get(author=self.request.user)
        if ad_author:
            participant = Participant.objects.filter(pk=param)
            if participant:
                participant.delete()
                # количество участников удаление из поле participant в объявлении
                count_participant = Participant.objects.filter(ad=my_ad).count()
                my_ad.participants = int(count_participant)
                my_ad.save()
                return JsonResponse({'status': 'success', 'message': 'Удаление прошло успешно'}, status=200)
                # удаление из комнаты чата

            else:
                raise ValidationError('Данный участник не существует.')
        else:
            raise ValidationError('Список участников пустой')
