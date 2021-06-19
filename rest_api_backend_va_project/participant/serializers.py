from rest_framework import serializers

from .models import Participant
from user.serializers import UserSerializers
from ad.serializers import AdSerializer


class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    ad = AdSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ('id', 'user', 'ad', 'number_of_person', 'number_of_girls', 'number_of_boys', 'create_ad')
