from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from events.models import Event, Platform, Category, Tag, Comment
from users.serializers import ArtistSerializer, CustomUserSerializer


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
        fields = ('id', 'name', 'description', 'location', 'support_phone')


class EventSerializer(serializers.ModelSerializer):
    cover = Base64ImageField(represent_in_base64=True, required=False)
    category = CategorySerializer(required=False)
    tags = TagSerializer(many=True, required=False)
    artists = ArtistSerializer(many=True, required=False)
    platform = PlatformSerializer(required=False)
    comments = CommentSerializer(many=True, required=False)
    tickets = CustomUserSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'cover', 'category', 'tags', 'description', 'age_limit', 'artists', 'platform', 
                  'video', 'price', 'total_tickets', 'tickets', 'open', 'when', 'comments')