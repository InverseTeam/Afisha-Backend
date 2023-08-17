from rest_framework import serializers
from events.models import *
from sber.settings import MEDIA_ROOT


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
        fields = ('id', 'name', 'description', 'address', 'location_data')


class EventImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = EventImage
        fields = ('id', 'image')


class EventReadSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    tags = TagSerializer(many=True, required=False)
    category = CategorySerializer(required=False)
    images = EventImageSerializer(many=True, required=False)
    platform = PlatformSerializer(required=False)


    class Meta:
        model = Event
        fields = ('id', 'name', 'cover', 'tags', 'category', 'description', 'age_limit', 'platform', 'date', 
                  'time', 'total_tickets', 'price', 'pushkin_payment', 'want_pushkin', 'artist', 'published', 'cover', 'images')
        

class EventWriteSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)


    class Meta:
        model = Event
        fields = ('id', 'name', 'cover', 'tags', 'category', 'description', 'age_limit', 'platform', 'date', 
                  'time', 'total_tickets', 'price', 'pushkin_payment', 'want_pushkin', 'artist', 'published', 'cover', 'images')
        

class EventTopicSerializer(serializers.ModelSerializer):
    events = EventReadSerializer(many=True, required=False)

    class Meta:
        model = EventTopic
        fields = ('id', 'name', 'description', 'events')