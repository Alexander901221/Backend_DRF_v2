from rest_framework import serializers
from .models import Ad
from user.serializers import UserSerializers, GetMeSerializer
from .models import User

class CreateAdSerializer(serializers.ModelSerializer):
    author = UserSerializers(read_only=True)

    class Meta:
        model = Ad
        fields = (
            'id', 'title', 'author', 'city', 'geolocation',
            'number_of_person', 'number_of_girls', 'number_of_boys',
            'party_date', 'is_published', 'create_ad'
        )


class AdSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source="get_city_display")
    author = UserSerializers(read_only=True)
    participants = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ad
        fields = (
            'id', 'title', 'author', 'city', 'geolocation',
            'number_of_person', 'number_of_girls', 'number_of_boys',
            'party_date', 'participants',
            # 'is_published', 'create_ad'
        )
        read_only_fields = fields


class UpdateAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = (
            'title', 'party_date', 'number_of_girls', 'number_of_boys'
        )


class GetMyDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = (
            'id', 'title', 'author', 'city', 'geolocation',
            'number_of_person', 'number_of_girls', 'number_of_boys',
            'party_date', 'participants',
            # 'is_published', 'create_ad'
        )
        read_only_fields = fields
