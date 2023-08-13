from django.contrib import admin
from events.models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'location', 'support_phone')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'attended')
    search_fields = ('id', 'user')
    list_filter = ('id', 'user', 'attended')


class EventImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'description', 'age_category', 'platform',
                    'start_date', 'end_date', 'tickets_number', 'tickets_sold', 'published')
    search_fields = ('id', 'name', 'category', 'age_category', 'platform')
    list_filter = ('id', 'name', 'category', 'age_category', 'platform', 'published')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating', 'comment_text')
    search_fields = ('id', 'user')
    list_filter = ('id', 'user', 'rating')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(EventImage, EventImageAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Comment, CommentAdmin)