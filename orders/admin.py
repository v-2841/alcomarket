from django.contrib import admin

from orders.models import Order, OrderGood


class GoodInline(admin.TabularInline):
    model = OrderGood

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.action(description='Отметить доставленными')
def set_is_delivered_to_true(modeladmin, request, queryset):
    queryset.update(is_delivered=True)


class OrderAdmin(admin.ModelAdmin):
    actions = [set_is_delivered_to_true]
    inlines = [GoodInline]
    readonly_fields = ['user', 'user_full_name', 'total_price']
    list_display = ('created_at', 'id', 'user', 'user_full_name',
                    'total_price', 'address', 'contact', 'is_delivered')
    ordering = ('is_delivered', '-created_at',)
    date_hierarchy = 'created_at'

    def user_full_name(self, obj):
        return obj.user.get_full_name()

    user_full_name.short_description = 'Полное имя'

    # def has_delete_permission(self, request, obj=None):
    #     return False


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderGood)
