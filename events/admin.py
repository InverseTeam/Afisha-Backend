from django.contrib import admin
from events.models import *


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'address', 'location_data')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class EventImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'description', 'age_limit', 'platform',
                    'date', 'time', 'total_tickets', 'price', 'pushkin_payment', 'want_pushkin', 'published', 'cover')
    search_fields = ('id', 'name', 'category', 'age_limit', 'platform', 'published')
    list_filter = ('name', 'category', 'age_limit', 'platform', 'published')


class EventTopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    search_fields = ('id', 'name', 'description')
    list_filter = ('name',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(EventImage, EventImageAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventTopic, EventTopicAdmin)