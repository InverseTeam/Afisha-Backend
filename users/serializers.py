from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Role
from events.serializers import EventReadSerializer


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'role_type')


class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    class Meta(BaseUserRegistrationSerializer.Meta):
        model = get_user_model()
        fields = ('email', 'firstname', 'lastname', 'age', 'role', 'password')


class CustomUserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(required=False)
    favorites = EventReadSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'firstname', 'lastname', 'favorites', 'age', 'role')


class CustomUserCurrentSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'firstname', 'lastname', 'age', 'role')