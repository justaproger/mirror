from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser

# Действие для изменения статуса активности пользователей
def set_active_status(modeladmin, request, queryset, is_active):
    users = CustomUser.objects.filter(groups__in=queryset)
    users.update(is_active=is_active)

# Действия для включения и отключения пользователей
def activate_users(modeladmin, request, queryset):
    set_active_status(modeladmin, request, queryset, True)
activate_users.short_description = "Activate all users in selected groups"

def deactivate_users(modeladmin, request, queryset):
    set_active_status(modeladmin, request, queryset, False)
deactivate_users.short_description = "Deactivate all users in selected groups"

# Кастомизация админки для пользователей
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('name',)
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

# Кастомизация админки для групп
class CustomGroupAdmin(admin.ModelAdmin):
    actions = [activate_users, deactivate_users]
    list_display = ('name', 'get_user_count')

    def get_user_count(self, obj):
        return obj.user_set.count()
    get_user_count.short_description = 'Number of Users'

# Регистрация кастомной админки для групп
admin.site.unregister(Group)
admin.site.register(Group, CustomGroupAdmin)