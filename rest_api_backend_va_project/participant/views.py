from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework.views import APIView
from .serializers import ParticipantSerializer
from ad.models import Ad
from django.db.models import Q
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


# Получение моих участников
# class MyParticipantsListAPIView(generics.ListAPIView):
#     serializer_class = ParticipantSerializer
#     permission_classes = []
#
#     def get_queryset(self):
#         return Participant.objects.filter(ad__author__pk=self.request.user.pk).only('ad__author')

class MyParticipantsListAPIView(APIView):
    serializer_class = ParticipantSerializer
    permission_classes = []

    def get_queryset(self):
        return Participant.objects.filter(ad__author__pk=self.request.user.pk).only('ad__author')

    def get(self, request, *args, **kwargs):
        ad_id = self.kwargs['pk']

        participant = Participant.objects.filtrer(Q(ad__author__pk=self.request.user.pk) & Q(ad__pk=ad_id))
        print('participant --> ', participant)

        return JsonResponse(
            {
                'status': "success",
                'message': "Ваша заявка успешно полученна",
                # 'data': list(bid)
            },
            status=status.HTTP_200_OK
        )


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
            return JsonResponse(
                {
                    'status': "error",
                    'message': "Данный пользователь уже находится в вашем списке участников"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
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
                return JsonResponse(
                    {
                        'status': "error",
                        'message': "Данного user нет в ваших заявках"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return JsonResponse(
                {
                    'status': "error",
                    'message': "У вас не созданного объявление"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


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
