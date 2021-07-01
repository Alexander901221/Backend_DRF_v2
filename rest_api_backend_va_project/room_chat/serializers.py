from rest_framework import serializers
from .models import Room
from ad.serializers import AdRoomChatSerializer
from user.serializers import UserRoomChatSerializer


class RoomSerializers(serializers.ModelSerializer):
    """Get request ===> that get_city_display works"""
    ad = AdRoomChatSerializer()
    invited = UserRoomChatSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        # fields = '__all__'
        fields = ['id', 'ad', 'invited']
