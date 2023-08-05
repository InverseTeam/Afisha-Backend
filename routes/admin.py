from django.contrib import admin
from routes.models import Route, RouteType


class RouteTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration', 'start_date', 'end_date', 'price', 'route_type', 'active')
    search_fields = ('id', 'name', 'duration')
    list_filter = ('id', 'name', 'duration')


admin.site.register(RouteType, RouteTypeAdmin)
admin.site.register(Route, RouteAdmin)
