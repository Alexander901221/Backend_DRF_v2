from rest_framework import generics, permissions, status
from django.http import JsonResponse

from .models import Ad
from .serializers import CreateAdSerializer, AdSerializer, UpdateAdSerializer, GetMyDataSerializer
from utils.send_letter_on_email.send_letter_on_email import Util
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from utils.exception_handling.exception_views import base_view


class AdListView(generics.ListAPIView):
    """Get all ads (GET)"""
    serializer_class = AdSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Ad.objects.all()\
        .defer("is_published", "create_ad", "author__password")\
        .select_related('author')


class AdRetrieveAPIView(generics.RetrieveAPIView):
    """Getting ad by param (GET)"""
    serializer_class = AdSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Ad.objects.all()\
        .defer("is_published", "create_ad", "author__password")\
        .select_related('author')


# Создание ad (post)
# class AdCreateView(generics.CreateAPIView):
#     serializer_class = CreateAdSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     queryset = Ad.objects.all()
#
#     def perform_create(self, serializer):
#         ad = Ad.objects.filter(author=self.request.user)
#         if ad:
#             raise ValidationError('У вас уже есть созданное объявления')
#         else:
#             user = self.request.user
#             # Отправка письма на почту о уведомление
#             email_body = 'Привет ' + user.username + '. Ваше объявление отправлено на модерацию. Если с ним все будет хорошо, оно будет опубликовано и в ближайшее время и появится на карте. Ответы будут приходить на электронную почту.'
#             email_subject = 'Создания объявления'
#             to_email = user.email
#             data_send_mail = {
#                 'email_body': email_body,
#                 'email_subject': email_subject,
#                 'to_email': to_email
#             }
#             Util.send_email(data=data_send_mail)
#             serializer.save(author=self.request.user)

class AdCreateView(APIView):
    """Create ad (post)"""
    # permission_classes = [permissions.IsAuthenticated]

    @base_view
    def post(self, request):
        data = JSONParser().parse(request)
        user = request.user

        author_ad = Ad.objects.filter(author=request.user)
        if author_ad:
            return JsonResponse(
                {
                    'status': 'error',
                    'message': 'У вас уже есть созданное объявления'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        print('author_ad ==> ', author_ad)
        Ad.objects.create(
            title=data['title'],
            author=request.user,
            city=data['city'],
            number_of_person=data['number_of_person'],
            number_of_girls=data['number_of_girls'],
            number_of_boys=data['number_of_boys'],
            party_date=data['party_date']
        )
        # Sending a letter to the mail about notification
        email_body = 'Привет ' + user.username + '. Ваше объявление отправлено на модерацию. ' \
                                                 'Если с ним все будет хорошо, оно будет опубликовано и ' \
                                                 'в ближайшее время и появится на карте. ' \
                                                 'Ответы будут приходить на электронную почту.'
        email_subject = 'Создания объявления'
        to_email = user.email
        data_send_mail = {
            'email_body': email_body,
            'email_subject': email_subject,
            'to_email': to_email
        }
        Util.send_email(data=data_send_mail)

        return JsonResponse(
            {
                'status': "success",
                'message': "Объявление успешно созданно"
            },
            status=status.HTTP_200_OK
        )


class AdUpdateView(generics.UpdateAPIView):
    """Update ad"""
    serializer_class = UpdateAdSerializer
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Ad.objects.all()


class AdDestroyAPIView(generics.DestroyAPIView):
    """Delete ad"""
    serializer_class = CreateAdSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @base_view
    def get_queryset(self):
        param = self.kwargs['pk']
        queryset = Ad.objects.filter(pk=param, author=self.request.user)
        return queryset

    @base_view
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance:
            instance.delete()
            return JsonResponse(
                {
                    'status': 'success',
                    'message': 'Удаление прошло успешно'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_destroy(instance)


class MyAdsListAPIView(generics.ListAPIView):
    """Get my ads"""
    serializer_class = GetMyDataSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @base_view
    def get_queryset(self):
        return Ad.objects\
            .defer("is_published", "create_ad", "author__password")\
            .filter(author__pk=7)
