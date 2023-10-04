from django.contrib import admin

from goods.models import Good


@admin.action(description='Сделать неактивным')
def set_active_to_false(modeladmin, request, queryset):
    queryset.update(active=False)


class GoodAdmin(admin.ModelAdmin):
    actions = [set_active_to_false]
    list_display = ('name', 'price', 'stock', 'category', 'manufacturer',
                    'active')
    ordering = ('-active', 'name')

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Good, GoodAdmin)
