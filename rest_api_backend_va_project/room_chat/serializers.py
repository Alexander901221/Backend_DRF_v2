from rest_framework import serializers
from .models import Room, Chat
from ad.serializers import AdRoomChatSerializer, CreateAdSerializer
from user.serializers import UserRoomChatSerializer


class RoomSerializers(serializers.ModelSerializer):
    """Get request ===> that get_city_display works"""
    ad = AdRoomChatSerializer()
    invited = UserRoomChatSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = ['id', 'ad', 'invited']


class ChatSerializer(serializers.ModelSerializer):
    user = UserRoomChatSerializer(read_only=True)
    class Meta:
        model = Chat
        fields = ('id', 'text', 'date', 'room', 'user')

