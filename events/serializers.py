from rest_framework import serializers
from events.models import *
from sber.settings import MEDIA_ROOT
from users.serializers import CustomUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(required=False)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'rating', 'comment_text')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id', 'name', 'description', 'location', 'support_phone')


class TicketSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(required=False)

    class Meta:
        model = Ticket
        fields = ('id', 'user', 'attended')
        

class EventImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = EventImage
        fields = ('id', 'image')


class EventReadSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    images = EventImageSerializer(many=True, required=False)
    category = CategorySerializer(required=False)
    platform = PlatformSerializer(required=False)
    comments = CommentSerializer(many=True, required=False)
    tickets = TicketSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'cover', 'category', 'description', 'age_category', 'platform', 
                  'comments', 'start_date', 'end_date', 'tickets_number', 'tickets_sold', 'tickets',
                  'published', 'cover', 'images')
        

class EventWriteSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    tickets = CustomUserSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'cover', 'category', 'description', 'age_category', 'platform', 
                  'comments', 'start_date', 'end_date', 'tickets_number', 'tickets_sold', 'tickets',
                  'published', 'cover', 'images')