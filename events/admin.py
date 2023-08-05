from django.contrib import admin
from django.utils.safestring import mark_safe
from events.models import Event, Platform, Tag, Category, Comment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class PlatformAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'location', 'support_phone')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'description', 'age_limit', 'platform', 'price', 'total_tickets', 'open', 'when', 'cover')
    search_fields = ('id', 'name', 'category', 'age_limit', 'total_tickets')
    list_filter = ('id', 'name', 'category', 'age_limit', 'total_tickets')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating', 'comment_text')
    search_fields = ('id', 'user')
    list_filter = ('id', 'user', 'rating')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Comment, CommentAdmin)
