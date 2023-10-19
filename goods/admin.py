from django.contrib import admin

from goods.models import Category, Good, Manufacturer, UserShoppingCart


@admin.action(description='Сделать неактивным')
def set_active_to_false(modeladmin, request, queryset):
    queryset.update(active=False)


class GoodAdmin(admin.ModelAdmin):
    actions = [set_active_to_false]
    list_display = ('name', 'normalize_volume', 'price', 'stock', 'category',
                    'manufacturer', 'purchase_count', 'active', 'created_at')
    ordering = ('-active', 'name')
    readonly_fields = ('purchase_count', 'created_at')

    @admin.display(description="Объем, л")
    def normalize_volume(self, obj):
        return obj.volume.normalize()

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('category', 'manufacturer')

    # def has_delete_permission(self, request, obj=None):
    #     return False


class UserShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user', 'good', 'quantity')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)


admin.site.register(Good, GoodAdmin)
admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(UserShoppingCart, UserShoppingCartAdmin)
