from rest_framework import serializers
from events.models import *
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
        fields = ('id', 'name', 'description', 'location', 'support_phone')


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ('id', 'sector', 'tickets_number', 'price')


class TicketSerializer(serializers.ModelSerializer):
    buyer = CustomUserSerializer()
    ticket_type = TicketTypeSerializer(required=False)

    class Meta:
        model = Ticket
        fields = ('id', 'buyer', 'ticket_type')


class PerformanceSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypeSerializer(many=True, required=False)
    tickets = TicketSerializer(many=True, required=False)

    class Meta:
        model = Performance
        fields = ('id', 'name', 'time', 'date', 'ticket_types', 'tickets')
        

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
    performances = PerformanceSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'category', 'tags', 'description', 'age_limit', 'platform', 'video',
                'tickets', 'open', 'entry_condition', 'artists', 'manager', 'comments', 'performances', 'cover', 'images')
        

class EventWriteSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    category = CategorySerializer(required=False)
    tags = TagSerializer(many=True, required=False)
    artists = ArtistSerializer(many=True, required=False)
    manager = CustomUserSerializer(required=False)
    platform = PlatformSerializer(required=False)
    comments = CommentSerializer(many=True, required=False)
    tickets = CustomUserSerializer(many=True, required=False)
    entry_condition = EntryConditionSerializer(required=False)

    class Meta:
        model = Event
        fields = ('id', 'name', 'category', 'tags', 'description', 'age_limit', 'platform', 'video',
                'tickets', 'open', 'entry_condition', 'artists', 'manager', 'comments', 'cover', 'images')