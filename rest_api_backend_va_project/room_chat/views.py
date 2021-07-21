from django.db.models import Q
from rest_framework import permissions, status
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RoomSerializers, ChatSerializer
from .models import Room, Chat
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from utils.mixins.pagination import PaginationHandlerMixin
from utils.permissions.permissions import EmailIsVerified, AccountIsVerified



class BasicPagination(PageNumberPagination):
    page_size_query_param = 'count'


class MyRooms(APIView):
    """Get all my rooms where i participant"""
    permission_classes = [AccountIsVerified]

    def get(self, request):
        rooms = Room.objects.all().filter(invited__pk=request.user.pk)
        if rooms:
            serializer = RoomSerializers(rooms, many=True)
            return Response({"data": serializer.data})
        else:
            return JsonResponse(
                {
                    'status': "error",
                    'message': "У вас пока нет комнат"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class Messages(APIView, PaginationHandlerMixin):
    """Get all messages for room"""
    permission_classes = [AccountIsVerified]
    pagination_class = BasicPagination

    def get(self, request, pk):
        messages = Chat.objects.all().filter(Q(room__pk=pk) & Q(room__invited__pk=request.user.pk))
        if messages:
            page = self.paginate_queryset(messages)
            if page is not None:
                serializer = self.get_paginated_response(ChatSerializer(page, many=True).data)
            else:
                serializer = ChatSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(
                {
                    'status': "error",
                    'message': "Данной комнаты не существует"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


def room(request, room_name):
    messages = Chat.objects.order_by('-date').filter(room__pk=room_name)[:10]
    print('messages (room) -> ', messages)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })


def get_my_rooms_2(request):
    rooms = Room.objects.filter(invited__pk=request.user.pk).values('pk')
    print('rooms (index) --> ', rooms)

    return JsonResponse(
        {
            'status': 'success',
            'message': rooms
        },
        status=status.HTTP_200_OK
    )
