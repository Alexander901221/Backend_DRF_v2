from rest_framework import generics, status, views
from django.http import JsonResponse
from django.db.models import Q, F
from rest_framework.views import APIView
from .models import Bid
from .serializers import BidSerializer, CreateBidSerializer, MyBidsSerializer
from ad.models import Ad
from participant.models import Participant
from loguru import logger


class BidRetrieveAPIView(APIView):
    """Get bid for pk"""
    serializer_class = BidSerializer
    # permission_classes = []

    @logger.catch
    def get(self, request, *args, **kwargs):
        ad_id = self.kwargs['ad_pk']
        print('ad_id --> ', ad_id)
        bid_id = self.kwargs['bid_pk']
        print('bid_id --> ', bid_id)

        ad = Bid.objects.filter(Q(ad__author__pk=request.user.pk) & Q(ad__pk=ad_id)).values('pk')

        bid = Bid.objects\
            .filter(Q(ad__author__pk=request.user.pk) & Q(pk=bid_id)) \
            .values(
                'id', 'photos', 'create_ad', 'author__id', 'author__username', 'author__photo'
            )

        if not ad:
            return JsonResponse(
                {
                    'status': "error",
                    'message': "У вас нет данного объявления"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not bid:
            return JsonResponse(
                {
                    'status': "error",
                    'message': "У вас нет данной заявки"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if ad and bid:
            return JsonResponse(
                {
                    'status': "success",
                    'message': "Ваша заявка успешно полученна",
                    'data': list(bid)
                },
                status=status.HTTP_200_OK
            )


class BidCreateView(views.APIView):
    """Create bid"""
    serializer_class = CreateBidSerializer
    # permission_classes = []

    @logger.catch
    def post(self, request, *args, **kwargs):
        data = self.request.data

        ad = Ad.objects.get(pk=data['id_ad'])
        participant = Participant.objects.filter(Q(user=self.request.user) & Q(ad__pk=data['id_ad'])).values('pk')
        check_bid = Bid.objects.filter(Q(author__pk=self.request.user.pk) & Q(ad__pk=data['id_ad'])).values('pk')

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

    @logger.catch
    def get(self, request, *args, **kwargs):
        id_ad = self.kwargs['pk']
        bids = Bid.objects \
            .filter(Q(ad__author__pk=self.request.user.pk) & Q(ad__pk=id_ad)) \
            .select_related('author', 'ad__author', 'ad') \
            .annotate(username=F('author__username'), photo=F('author__photo'))\
            .values('id', 'username', 'photo')

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
                status=status.HTTP_404_NOT_FOUND
            )


class BidRejected(generics.DestroyAPIView):
    """Rejected bid"""
    serializer_class = BidSerializer
    # permission_classes = []

    @logger.catch
    def delete(self, request, *args, **kwargs):
        param = self.kwargs['pk']
        bid = Bid.objects.filter(Q(pk=param) & Q(ad__author__pk=self.request.user.pk))

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
                status=status.HTTP_200_OK
            )
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Данной заявки не существует'
                },
                status=status.HTTP_404_NOT_FOUND
            )


from django.views.generic import TemplateView
class BidView(TemplateView):
    template_name = "bid.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
