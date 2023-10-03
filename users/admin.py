from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff',)
    ordering = ('username',)
    fieldsets = (
        (None, {
            'fields': ('username', 'password')}),
        ('Персональные данные', {
            'fields': ('first_name', 'last_name', 'email')}),
        ('Права пользователя', {
            'fields': ('is_active', 'is_staff',
                       'is_superuser',)}),
        ('Важные даты', {
            'fields': ('last_login', 'date_joined')}),
    )


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
