import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework import permissions, serializers
from django.db.models.fields import CharField
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from events.models import Event, EventImage, Platform, Category, Tag, Comment, EntryCondition
from sber.settings import MEDIA_ROOT
from users.serializers import ArtistSerializer, CustomUserSerializer


class EntryConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryCondition
        fields = ('id', 'name')


class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(required=False)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'rating', 'comment_text')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class CategorySerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = ('id', 'name', 'tags')


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id', 'name', 'description', 'location', 'support_phone')\
        

class EventImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = EventImage
        fields = ('id', 'image')


class EventReadSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    images = EventImageSerializer(many=True, required=False)
    category = CategorySerializer(required=False)
    tags = TagSerializer(many=True, required=False)
    artists = ArtistSerializer(many=True, required=False)
    platform = PlatformSerializer(required=False)
    comments = CommentSerializer(many=True, required=False)
    tickets = CustomUserSerializer(many=True, required=False)
    entry_condition = EntryConditionSerializer(required=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'category', 'tags', 'description', 'age_limit', 'artists', 'platform', 
                  'video', 'price', 'total_tickets', 'tickets', 'open', 'when', 'entry_condition', 'comments', 'cover', 'images')
        

class EventWriteSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    category = CategorySerializer(required=False)
    tags = TagSerializer(many=True, required=False)
    artists = ArtistSerializer(many=True, required=False)
    platform = PlatformSerializer(required=False)
    comments = CommentSerializer(many=True, required=False)
    tickets = CustomUserSerializer(many=True, required=False)
    entry_condition = EntryConditionSerializer(required=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'category', 'tags', 'description', 'age_limit', 'artists', 'platform', 
                  'video', 'price', 'total_tickets', 'tickets', 'open', 'when', 'entry_condition', 'comments', 'cover', 'images')