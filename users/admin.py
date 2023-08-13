from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.forms import UserChangeForm, UserCreationForm
from users.models import CustomUser, Role


class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'role_type')
    search_fields = ('id', 'name', 'role_type')
    list_filter = ('name',)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('id', 'username', 'email', 'firstname', 'lastname', 'role', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'firstname', 'lastname', 'role', 'password')}),
        ('Permissions', {'fields': ('is_superuser',)}),)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'firstname', 'lastname', 'role', 'password1', 'password2'),
        }),)
    search_fields = ('username', 'email',)
    ordering = ('username', 'email',)
    filter_horizontal = ()


admin.site.register(Role, RoleAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)