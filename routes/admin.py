from routes.models import Route, CustomRoute
from django.contrib import admin


class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration', 'distance')
    search_fields = ('id', 'name', 'duration', 'distance')
    list_filter = ('name', 'duration', 'distance')
    

class CustomRouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'duration', 'distance')
    search_fields = ('id', 'duration', 'distance')
    list_filter = ('duration', 'distance')


admin.site.register(Route, RouteAdmin)
admin.site.register(CustomRoute, CustomRouteAdmin)
