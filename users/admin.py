from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.forms import UserChangeForm, UserCreationForm
from users.models import CustomUser, Role, Artist


class ArtistAdmin(admin.ModelAdmin):
    list_display = ('id', 'nickname', 'bio', 'firstname', 'lastname', 'surname', 'artist_type', 'manager')
    search_fields = ('id', 'nickname')
    list_filter = ('id', 'nickname')


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role_id')
    search_fields = ('id', 'name', 'role_id')
    list_filter = ('name',)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'email', 'phone_number', 'firstname', 'lastname', 'age', 'role', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'firstname', 'lastname', 'age', 'role', 'password')}),
        ('Permissions', {'fields': ('is_superuser',)}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'firstname', 'lastname', 'age', 'role', 'password1', 'password2'),
        }),)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(Artist, ArtistAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)