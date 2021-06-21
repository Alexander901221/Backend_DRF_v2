from rest_framework import generics, status
from django.http import JsonResponse
from rest_framework.views import APIView
from .serializers import ParticipantSerializer
from ad.models import Ad
from django.db.models import Q
from bid.models import Bid
from user.models import User

# Добавление в комнату
from participant.models import Participant


class ParticipantRetrieveAPIView(generics.RetrieveAPIView):
    """Get participant for ad and bid"""
    serializer_class = ParticipantSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        ad_id = self.kwargs['ad_pk']
        participant_id = self.kwargs['participant_pk']

        ad = Participant.objects.filter(Q(ad__author__pk=request.user.pk) & Q(ad__pk=ad_id)).values('pk')

        participant = Participant.objects \
            .filter(Q(ad__author__pk=request.user.pk) & Q(pk=participant_id)) \
            .values(
            'id', 'number_of_person', 'number_of_girls', 'number_of_boys', 'photos', 'create_ad',
            'user__id', 'user__username', 'user__photo', 'user__sex'
        )

        if not ad:
            return JsonResponse(
                {
                    'status': "error",
                    'message': "У вас нет данного объявления"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not participant:
            return JsonResponse(
                {
                    'status': "error",
                    'message': "У вас нет данного участника"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if ad and participant:
            return JsonResponse(
                {
                    'status': "success",
                    'message': "Ваша заявка успешно полученна",
                    'data': list(participant)
                },
                status=status.HTTP_200_OK
            )


class MyParticipantsListAPIView(APIView):
    """Get all my participants"""
    serializer_class = ParticipantSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs):
        ad_id = self.kwargs['pk']

        participant = Participant.objects \
            .filter(Q(ad__author__pk=self.request.user.pk) & Q(ad__pk=ad_id)) \
            .values(
            'id', 'number_of_person', 'number_of_girls', 'number_of_boys', 'photos', 'create_ad',
            'user__id', 'user__username', 'user__photo', 'user__sex'
        )
        if participant.exists():
            return JsonResponse(
                {
                    'status': "success",
                    'message': "Ваша заявка успешно полученна",
                    'data': list(participant)
                },
                status=status.HTTP_200_OK
            )
        else:
            return JsonResponse(
                {
                    'status': "error",
                    'message': "У вас нет участников"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ParticipantCreateView(generics.CreateAPIView):
    """Add participant"""
    serializer_class = ParticipantSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_id = self.request.data['id_user']
        ad_id = self.request.data['id_ad']

        my_ad = Ad.objects.get(Q(author__pk=self.request.user.pk) & Q(pk=ad_id))

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
            check_user_bid = Bid.objects \
                .filter(author__pk=user_id, ad__author__pk=self.request.user.pk)

            if check_user_bid:
                for bid in check_user_bid.values('number_of_person', 'number_of_girls', 'number_of_boys', 'photos'):

                    participant = Participant.objects\
                        .filter(Q(ad__author__pk=request.user.pk) & Q(ad__pk=ad_id) & Q(user=user_id))
                    if participant:
                        return JsonResponse(
                            {
                                "status": "success",
                                "message": "У вас уже есть в участниках данный пользователь"
                            },
                            status=status.HTTP_404_NOT_FOUND
                        )
                    else:
                        participant.create(
                            user=user,
                            ad=my_ad,
                            number_of_person=int(bid['number_of_person']),
                            number_of_girls=int(bid['number_of_girls']),
                            number_of_boys=int(bid['number_of_boys']),
                            photos=bid['photos']
                        )

                check_user_bid.delete()

                # Количество участников добавляется в поле participant в объявлении
                count_participant = Participant.objects.filter(ad=my_ad).count()
                my_ad.participants = int(count_participant)
                my_ad.save()

                return JsonResponse(
                    {
                        "status": "success",
                        "message": "Вы успешно добавили пользователя в список участников"
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return JsonResponse(
                    {
                        'status': "error",
                        'message': "Данного user нет в ваших заявках"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return JsonResponse(
                {
                    'status': "error",
                    'message': "У вас не созданного объявление"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class ParticipantDestroyAPIView(generics.DestroyAPIView):
    """Reject participant"""
    serializer_class = ParticipantSerializer
    permission_classes = []
    queryset = Participant.objects.all()

    def delete(self, request, *args, **kwargs):
        ad_id = kwargs['ad_pk']
        participant_id = kwargs['participant_pk']

        user = self.request.user.pk
        participant = Participant.objects.filter(Q(ad__author__pk=user) & Q(ad__pk=ad_id) & Q(pk=participant_id))
        my_ad = Ad.objects.get(author__pk=user)

        if participant:
            participant.delete()
            # количество участников удаление из поле participant в объявлении
            count_participant = Participant.objects.filter(ad=my_ad).count()
            my_ad.participants = int(count_participant)
            my_ad.save()
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Удаление прошло успешно'
                },
                status=status.HTTP_200_OK
            )
            # удаление из комнаты чата
            #
            #
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Данного участника нет у вас в списке'
                },
                status=status.HTTP_404_NOT_FOUND
            )
