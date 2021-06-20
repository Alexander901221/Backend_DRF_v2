from rest_framework import generics, status, views
from django.http import JsonResponse
from django.db.models import Q
from rest_framework.views import APIView
from .models import Bid
from .serializers import BidSerializer, CreateBidSerializer, MyBidsSerializer
from ad.models import Ad
from participant.models import Participant


class BidRetrieveAPIView(generics.RetrieveAPIView):
    """Get bid for pk"""
    serializer_class = BidSerializer
    # permission_classes = []
    queryset = Bid.objects.all().select_related('author', 'ad__author', 'ad')


class BidCreateView(views.APIView):
    """Create bid"""
    serializer_class = CreateBidSerializer
    # permission_classes = []

    def post(self, request, *args, **kwargs):
        data = self.request.data

        ad = Ad.objects.get(pk=data['id_ad'])
        participant = Participant.objects.filter(Q(user=self.request.user) & Q(ad__pk=data['id_ad'])).values('id')
        check_bid = Bid.objects.filter(Q(author__pk=self.request.user.pk) & Q(ad__pk=data['id_ad'])).values('id')

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


class MyBidsRetrieveAPIView(APIView):
    """Get all my bids for ad"""
    serializer_class = MyBidsSerializer

    def get(self, request, *args, **kwargs):
        id_ad = self.kwargs['pk']
        bids = Bid.objects \
            .filter(Q(ad__author__pk=self.request.user.pk) & Q(ad__pk=id_ad)) \
            .select_related('author', 'ad__author', 'ad') \
            .values('author', 'number_of_person', 'number_of_girls', 'number_of_boys', 'photos', 'create_ad')

        if bids:
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Ваши заявки успешно получены',
                    'data': list(bids)
                },
                status=status.HTTP_200_OK
            )
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'У вас пока нет заявок'
                },
                status=200
            )


class BidRejected(generics.DestroyAPIView):
    """rejected bid"""
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
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Данная заявка успешно отклонена'
                 },
                status=200
            )
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Данной заявки не существует'
                },
                status=400
            )
