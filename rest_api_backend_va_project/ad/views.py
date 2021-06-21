from django.db.models import Q
from rest_framework import generics, permissions, status
from django.http import JsonResponse

from .models import Ad
from .serializers import CreateAdSerializer, AdSerializer, UpdateAdSerializer, GetMyDataSerializer
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from loguru import logger


class AdListView(generics.ListAPIView):
    """Get all ads (GET)"""
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    @logger.catch
    def get_queryset(self):
        return Ad.objects.all().defer("is_published", "create_ad", "author__password").select_related('author')


class AdRetrieveAPIView(generics.RetrieveAPIView):
    """Getting ad by param (GET)"""
    serializer_class = AdSerializer
    permission_classes = [permissions.IsAuthenticated]

    @logger.catch
    def get_queryset(self):
        return Ad.objects.all().defer("is_published", "create_ad", "author__password").select_related('author')


class AdCreateView(APIView):
    """Create ad (post)"""
    permission_classes = [permissions.IsAuthenticated]

    @logger.catch
    def post(self, request):
        data = request.data
        user = request.user

        author_ad = Ad.objects.filter(author__pk=user.pk).values('pk')
        if author_ad:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'У вас уже есть созданное объявления'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        author_ad.create(
            title=data['title'],
            author=user,
            geolocation=data['geolocation'],
            city=data['city'],
            number_of_person=data['number_of_person'],
            number_of_girls=data['number_of_girls'],
            number_of_boys=data['number_of_boys'],
            party_date=data['party_date']
        )

        # WebSocket notification ("Объявление успешно созданно")

        return JsonResponse(
            {
                'status': "success",
                'message': "Объявление успешно созданно и отправлено на модерацию. "
                           "Если с ним все будет хорошо, оно будет опубликовано и появится на карте."
            },
            status=status.HTTP_200_OK
        )


class AdUpdateView(generics.UpdateAPIView):
    """Update ad"""
    serializer_class = UpdateAdSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Ad.objects.all().select_related('author')

    @logger.catch
    def put(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        param = kwargs['pk']
        ad = Ad.objects.filter(Q(pk=param) | Q(author__pk=request.user.pk))

        if ad.exists():
            ad.update(
                title=data['title'],
                city=data['city'],
                geolocation=data['geolocation'],
                number_of_person=data['number_of_person'],
                number_of_girls=data['number_of_girls'],
                number_of_boys=data['number_of_boys'],
                party_date=data['party_date'],
                is_published=False
            )
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Объявление успешно обновленно и отправлено на модерацию. '
                               'Если с ним все будет хорошо, оно будет опубликовано и появится на карте.',
                    'data': {
                        'title': data['title'],
                        'city': data['city'],
                        'geolocation': data['geolocation'],
                        'number_of_person': data['number_of_person'],
                        'number_of_girls': data['number_of_girls'],
                        'number_of_boys': data['number_of_boys'],
                        'party_date': data['party_date']
                    }
                },
                status=status.HTTP_200_OK
            )
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Данного объявления не существует'
                },
                status=status.HTTP_200_OK
            )


class AdDestroyAPIView(generics.DestroyAPIView):
    """Delete ad"""
    serializer_class = CreateAdSerializer

    permission_classes = [permissions.IsAuthenticated]

    @logger.catch
    def destroy(self, request, *args, **kwargs):
        param = kwargs['pk']

        ad = Ad.objects.filter(Q(pk=param) & Q(author__pk=request.user.pk))

        if ad.exists():
            ad.delete()

            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Ваше объявление успешно удаленно'
                },
                status=status.HTTP_200_OK
            )
        else:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'Данного объявления не существует'
                },
                status=status.HTTP_200_OK
            )


class MyAdsListAPIView(generics.ListAPIView):
    """Get my ads"""
    serializer_class = GetMyDataSerializer

    permission_classes = [permissions.IsAuthenticated]

    @logger.catch
    def get_queryset(self):
        return Ad.objects \
            .defer("create_ad", "author__password") \
            .filter(author__pk=self.request.user.pk)
