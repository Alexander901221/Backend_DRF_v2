from django.db.models import Q
from rest_framework import generics, permissions, status
from django.http import JsonResponse

from .models import Ad
from user.models import User
from room_chat.models import Room
from .serializers import CreateAdSerializer, AdSerializer, UpdateAdSerializer, GetMyDataSerializer, GetAllAdsForMap
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from loguru import logger
import json
from utils.permissions.permissions import EmailIsVerified, AccountIsVerified


class AdListView(generics.ListAPIView):
    """Get all ads (GET)"""
    serializer_class = GetAllAdsForMap
    permission_classes = [EmailIsVerified]

    @logger.catch
    def get_queryset(self):
        return Ad.custom_manager\
            .custom_filter(city=self.request.user.city)\
            .only('id', 'geolocation')


def to_json(obj):
    return {
        'id': obj.pk,
        'photo': '/images/' + str(obj.photo)
    }

class AdRetrieveAPIView(generics.ListAPIView):
    """Getting ad by param (GET)"""
    serializer_class = AdSerializer
    permission_classes = [EmailIsVerified]
    
    @logger.catch
    def get(self, request, *args, **kwargs):
        ad = Ad.custom_manager.custom_filter().get(id=kwargs['pk'], city=self.request.user.city)

        participant = []
        for element in ad.participants.all():
            result = to_json(element)
            participant.append(result)

        if ad:
            return JsonResponse(
                    {
                        'status': 'success',
                        "ad": {
                            "id": ad.pk,
                            "title": ad.title,
                            "author": {
                                "id": ad.author.pk,
                                "photo": '/images/' + str(ad.author.photo)
                            },                        
                            "number_of_person": ad.number_of_person,
                            "number_of_girls": ad.number_of_girls,
                            "number_of_boys": ad.number_of_boys,
                            "party_date": json.dumps(ad.party_date, indent=4, sort_keys=True, default=str),
                            "participants": participant,
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
                        status=status.HTTP_400_BAD_REQUEST
            )
        

class AdCreateView(APIView):
    """Create ad (post)"""
    permission_classes = [AccountIsVerified]

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

        ad = author_ad.create(
            title=data['title'],
            author=user,
            geolocation=data['geolocation'],
            city=data['city'],
            number_of_person=data['number_of_person'],
            number_of_girls=data['number_of_girls'],
            number_of_boys=data['number_of_boys'],
            party_date=data['party_date']
        )

        ad.participants.add(User.objects.get(pk=user.pk))

        # Create room, and add author in the room
        room = Room.objects.create(ad=ad)
        room.invited.add(user)

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
    permission_classes = [AccountIsVerified]
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

    permission_classes = [AccountIsVerified]

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

    permission_classes = [AccountIsVerified]

    @logger.catch
    def get_queryset(self):
        return Ad.custom_manager.custom_order_by('party_date') \
            .defer("create_ad", "author__password") \
            .filter(author__pk=self.request.user.pk)


# Notification
from django.views.generic import TemplateView


class AdView(TemplateView):
    template_name = "ad.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
