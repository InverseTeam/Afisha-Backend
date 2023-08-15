from rest_framework import serializers
from events.models import *
from sber.settings import MEDIA_ROOT
from users.serializers import CustomUserSerializer


class ArtistTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistType
        fields = ('id', 'name')


class ArtistSerializer(serializers.ModelSerializer):
    artist_type = ArtistTypeSerializer()

    class Meta:
        model = Artist
        fields = ('id', 'nickname', 'bio', 'firstname', 'lastname', 'surname', 'artist_type')


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
        fields = ('id', 'xid', 'name', 'description', 'location', 'support_phone')


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = ('id', 'sector', 'price', 'tickets_number', 'tickets_sold', 'open')


class PerformanceSerializer(serializers.ModelSerializer):
    ticket_types = TicketTypeSerializer(many=True, required=False)

    class Meta:
        model = Performance
        fields = ('id', 'name', 'time', 'date', 'ticket_types', 'tickets', 'open')


class TicketReadSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(required=False)
    ticket_type = TicketTypeSerializer(required=False)
    performance = PerformanceSerializer(required=False)

    class Meta:
        model = Ticket
        fields = ('id', 'user', 'ticket_type', 'performance', 'attended')


class TicketWriteSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(required=False)

    class Meta:
        model = Ticket
        fields = ('id', 'user', 'ticket_type', 'performance', 'attended')
        

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
    tickets = TicketReadSerializer(many=True, required=False)
    artists = ArtistSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, required=False)


    class Meta:
        model = Event
        fields = ('id', 'name', 'cover', 'tags', 'category', 'description', 'age_limit', 'platform', 
                  'comments', 'start_date', 'end_date', 'tickets', 'artists', 'performances', 'open', 
                  'cover', 'images')
        

class EventWriteSerializer(serializers.ModelSerializer):
    cover = serializers.ImageField(required=False)
    tickets = CustomUserSerializer(many=True, required=False)


    class Meta:
        model = Event
        fields = ('id', 'name', 'cover', 'tags', 'category', 'description', 'age_limit', 'platform', 
                  'comments', 'start_date', 'end_date', 'tickets', 'artists', 'performances', 'open', 
                  'cover', 'images')