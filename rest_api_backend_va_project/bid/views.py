from rest_framework import generics, status, views
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from django.db.models import Q

from .models import Bid
from .serializers import BidSerializer, CreateBidSerializer
from ad.models import Ad
from participant.models import Participant


# Получение всех bids (GET)
class BidListView(generics.ListAPIView):
    serializer_class = BidSerializer
    # permission_classes = []
    queryset = Bid.objects.all().select_related('author', 'ad__author', 'ad')


# Получение bid по param (GET)
class BidRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = BidSerializer
    # permission_classes = []
    queryset = Bid.objects.all().select_related('author', 'ad__author', 'ad')


# Создание bid (post)
# class BidCreateView(generics.CreateAPIView):
#     serializer_class = BidSerializer
#     # permission_classes = []
#     # queryset = Bid.objects.all()
#
#     def perform_create(self, serializer):
#         id_ad = self.request.data['id_ad']
#         ad = Ad.objects.get(pk=id_ad)
#         bid = Bid.objects.filter(author=self.request.user, ad__pk=id_ad)
#         if bid:
#             raise ValidationError('Вы уже подали заявку. Дождитесь ответа')
#         else:
#             serializer.save(author=self.request.user, ad=ad)


class BidCreateView(views.APIView):
    serializer_class = CreateBidSerializer

    # permission_classes = []

    def post(self, request, *args, **kwargs):
        data = self.request.data

        ad = Ad.objects.get(pk=data['id_ad'])
        participant = Participant.objects.filter(Q(user=self.request.user) & Q(ad__pk=data['id_ad']))

        check_bid = Bid.objects.filter(Q(author__pk=self.request.user.pk) & Q(ad__pk=data['id_ad']))

        if check_bid or participant:
            return JsonResponse(
                {
                    'status': "error",
                    'message': "Вы уже подали заявку. Дождитесь ответа автора."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            check_bid.create(
                author=self.request.user,
                ad=ad,
                number_of_person=data['number_of_person'],
                number_of_girls=data['number_of_girls'],
                number_of_boys=data['number_of_boys'],
                photos=data['photos']
            )

        return JsonResponse(
            {
                'status': "success",
                'message': "Заявка успешно одобренна"
            },
            status=status.HTTP_200_OK
        )


# Обновление bid (put)
class BidUpdateView(generics.UpdateAPIView):
    serializer_class = BidSerializer
    # permission_classes = []
    queryset = Bid.objects.all()


# Получение всех моих заявок по моему объявлению
class MyBidsListAPIView(generics.ListAPIView):
    serializer_class = BidSerializer

    # permission_classes = []

    def get_queryset(self):
        bids = Bid.objects \
            .filter(ad__author__pk=self.request.user.pk) \
            .select_related('author', 'ad__author', 'ad')

        if bids:
            return bids
        else:
            raise ValidationError('У вас пока нет заявок')


# Отказ заявке
class BidRejected(generics.DestroyAPIView):
    serializer_class = BidSerializer
    # permission_classes = []
    queryset = Bid.objects.all()

    def delete(self, request, *args, **kwargs):
        param = self.kwargs['pk']
        bid = Bid.objects.filter(Q(pk=param) & Q(ad__author=self.request.user))
        if bid:
            bid.delete()
            """
                Уведомление user о том, что его заявку отклонили ( Websocket )
            """
            return JsonResponse({'status': 'success', 'message': 'Удаление прошло успешно'}, status=200)
        else:
            raise ValidationError('Данной заявки не существует.')
