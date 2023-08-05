from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Artist, ArtistType


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = get_user_model()
        fields = ('email', 'firstname', 'lastname', 'age', 'role', 'password')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'firstname', 'lastname', 'age', 'money', 'role')


class CustomUserCurrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'firstname', 'lastname', 'age', 'money', 'role')


class ArtistTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistType
        fields = ('id', 'name')


class ArtistSerializer(serializers.ModelSerializer):
    manager = CustomUserSerializer()
    artist_type = ArtistTypeSerializer()

    class Meta:
        model = Artist
        fields = ('id', 'nickname', 'bio', 'firstname', 'lastname', 'surname', 'artist_type', 'manager')