import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework import permissions, serializers
from django.db.models.fields import CharField
from drf_extra_fields.fields import Base64ImageField, Base64FileField
from events.models import Event, Platform, Category, Tag, Comment, EntryCondition
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


class EventSerializer(serializers.ModelSerializer):
    cover = serializers.CharField(max_length=None, required=False, allow_blank=True)
    category = CategorySerializer(required=False)
    tags = TagSerializer(many=True, required=False)
    artists = ArtistSerializer(many=True, required=False)
    platform = PlatformSerializer(required=False)
    comments = CommentSerializer(many=True, required=False)
    tickets = CustomUserSerializer(many=True, required=False)
    entry_condition = EntryConditionSerializer(required=False)

    def save(self):
        svg_data = self.validated_data.get('cover', None)
        event = Event(**self.validated_data)
    
        if svg_data:
            svg_bytes = base64.b64decode(svg_data)
            svg_name = str(uuid.uuid4())

            event.cover.save(f'{svg_name}.svg', ContentFile(svg_bytes), save=True)
        
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
                  'video', 'price', 'total_tickets', 'tickets', 'open', 'when', 'entry_condition', 'comments', 'cover')
        
        
