from django.contrib import admin
from events.models import *


class EntryConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')
    

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


class TicketTypeAdmin(admin.ModelAdmin):
    list_filter = ('id', 'sector', 'tickets_number', 'price')
    search_fields = ('id', 'sector', 'price')
    list_filter = ('id', 'sector', 'price')


class TicketAdmin(admin.ModelAdmin):
    list_filter = ('id', 'buyer', 'ticket_type')
    search_fields = ('id', 'buyer', 'ticket_type')
    list_filter = ('id', 'buyer', 'ticket_type')


class PerformanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'time', 'date')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class EventImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'description', 'age_limit', 'platform', 'open', 'cover', 'manager')
    search_fields = ('id', 'name', 'category', 'age_limit', 'manager')
    list_filter = ('id', 'name', 'category', 'age_limit', 'manager')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating', 'comment_text')
    search_fields = ('id', 'user')
    list_filter = ('id', 'user', 'rating')


admin.site.register(EntryCondition, EntryConditionAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(TicketType, TicketTypeAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Performance, PerformanceAdmin)
admin.site.register(EventImage, EventImageAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Comment, CommentAdmin)