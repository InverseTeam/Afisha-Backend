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

    class Meta:
        model = EventImage
        fields = ('id', 'image')


class EventSerializer(serializers.ModelSerializer):
    cover = serializers.CharField(max_length=None, required=False, allow_blank=True)
    images = serializers.CharField(max_length=None, required=False, allow_blank=True)
    category = CategorySerializer(required=False)
    tags = TagSerializer(many=True, required=False)
    artists = ArtistSerializer(many=True, required=False)
    platform = PlatformSerializer(required=False)
    comments = CommentSerializer(many=True, required=False)
    tickets = CustomUserSerializer(many=True, required=False)
    entry_condition = EntryConditionSerializer(required=False)

    def save(self):
        svg_data = self.validated_data.get('cover', None)
        images_data = self.validated_data.get('images', None)
        
        if images_data:
            self.validated_data.pop('images')

        event = Event(**self.validated_data)
    
        if svg_data:
            svg_bytes = base64.b64decode(svg_data)
            svg_name = str(uuid.uuid4())

            event.cover.save(f'{svg_name}.svg', ContentFile(svg_bytes), save=True)

        if images_data:
            images_data_list = images_data.split('<<<base64_image>>>')[1:]
            
            for image in images_data_list:
                image_bytes = base64.b64decode(image)
                image_name = str(uuid.uuid4())
                event_image = EventImage()

                event_image.image.save(f'{image_name}.svg', ContentFile(image_bytes), save=True)
                event_image.save()

                event.images.add(event_image.pk)

        event.save()
    
        return {'message': 'success'}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        base64_representation = {}

        for field_name, value in representation.items():
            if field_name in ['cover'] and self.context.get('request').method in permissions.SAFE_METHODS:
                if value:
                    if isinstance(value, str):
                            svg_bytes = value.encode('utf-8')
                    elif isinstance(value, int):
                        svg_bytes = str(value).encode('utf-8')
                    else:
                        raise serializers.ValidationError("Invalid data type. String or integer expected.")

                    with open(f'{MEDIA_ROOT}{svg_bytes.decode("utf-8")}', 'rb') as f:
                        base64_data = base64.standard_b64encode(f.read()).decode('utf-8')
                        base64_representation[field_name] = base64_data
            else:
                base64_representation[field_name] = value

        return base64_representation


    class Meta:
        model = Event
        fields = ('id', 'name', 'category', 'tags', 'description', 'age_limit', 'artists', 'platform', 
                  'video', 'price', 'total_tickets', 'tickets', 'open', 'when', 'entry_condition', 'comments', 'cover', 'images')


class EventCorrectSerializer(serializers.ModelSerializer):
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


class EventReadSerializer(serializers.ModelSerializer):
    cover = serializers.CharField(max_length=None, required=False, allow_blank=True)
    category = CategorySerializer(required=False)
    tags = TagSerializer(many=True, required=False)
    artists = ArtistSerializer(many=True, required=False)
    platform = PlatformSerializer(required=False)
    comments = CommentSerializer(many=True, required=False)
    tickets = CustomUserSerializer(many=True, required=False)
    entry_condition = EntryConditionSerializer(required=False)


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        base64_representation = {}

        for field_name, value in representation.items():
            if field_name in ['cover']:
                if value:
                    if isinstance(value, str):
                            svg_bytes = value.encode('utf-8')

                    elif isinstance(value, int):
                        svg_bytes = str(value).encode('utf-8')

                    else:
                        raise serializers.ValidationError("Invalid data type. String or integer expected.")

                    with open(f'{MEDIA_ROOT}{svg_bytes.decode("utf-8")}', 'rb') as f:
                        base64_data = base64.standard_b64encode(f.read()).decode('utf-8')
                        base64_representation[field_name] = base64_data

            elif field_name in ['images']:
                base64_images = ''

                for image_base64 in list(value):
                    image_base64 = EventImage.objects.get(pk=image_base64)

                    if isinstance(str(image_base64.image), str):
                        svg_bytes = str(image_base64.image).encode('utf-8')

                    elif isinstance(int(image_base64), int):
                        svg_bytes = str(image_base64.image).encode('utf-8')

                    else:
                        raise serializers.ValidationError("Invalid data type. String or integer expected.")
                    
                    with open(f'{MEDIA_ROOT}{svg_bytes.decode("utf-8")}', 'rb') as f:
                        base64_data = base64.standard_b64encode(f.read()).decode('utf-8')
                        base64_images += '<<<base64_image>>>' + base64_data

                base64_representation[field_name] = base64_images

            else:
                base64_representation[field_name] = value

        return base64_representation


    class Meta:
        model = Event
        fields = ('id', 'name', 'category', 'tags', 'description', 'age_limit', 'artists', 'platform', 
                  'video', 'price', 'total_tickets', 'tickets', 'open', 'when', 'entry_condition', 'comments', 'cover', 'images')
        

class EventWriteSerializer(serializers.ModelSerializer):
    cover = serializers.CharField(max_length=None, required=False, allow_blank=True)
    images = serializers.CharField(max_length=None, required=False, allow_blank=True)
    category = CategorySerializer(required=False)
    tags = TagSerializer(many=True, required=False)
    artists = ArtistSerializer(many=True, required=False)
    platform = PlatformSerializer(required=False)
    comments = CommentSerializer(many=True, required=False)
    tickets = CustomUserSerializer(many=True, required=False)
    entry_condition = EntryConditionSerializer(required=False)

    def save(self):
        svg_data = self.validated_data.get('cover', None)
        images_data = self.validated_data.get('images', None)
        
        if images_data:
            self.validated_data.pop('images')

        event = Event(**self.validated_data)
    
        if svg_data:
            svg_bytes = base64.b64decode(svg_data)
            svg_name = str(uuid.uuid4())

            event.cover.save(f'{svg_name}.svg', ContentFile(svg_bytes), save=True)

        if images_data:
            images_data_list = images_data.split('<<<base64_image>>>')
            
            for image in images_data_list:
                image_bytes = base64.b64decode(image)
                image_name = str(uuid.uuid4())
                event_image = EventImage()

                event_image.image.save(f'{image_name}.svg', ContentFile(image_bytes), save=True)
                event_image.save()

                event.images.add(event_image.pk)

        event.save()
    
        return {'message': 'success'}

    class Meta:
        model = Event
        fields = ('id', 'name', 'category', 'tags', 'description', 'age_limit', 'artists', 'platform', 
                  'video', 'price', 'total_tickets', 'tickets', 'open', 'when', 'entry_condition', 'comments', 'cover', 'images')