from rest_framework import generics, permissions, views, status
from .serializers import RoomSerializers
from .models import Room


class RoomListView(generics.ListAPIView):
    serializer_class = RoomSerializers
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Room.objects.all()
