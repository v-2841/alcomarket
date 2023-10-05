from django.contrib import admin

from orders.models import Order, OrderGood


class GoodInline(admin.TabularInline):
    model = OrderGood
    min_num = 1


class OrderAdmin(admin.ModelAdmin):
    inlines = [GoodInline]
    readonly_fields = ['total_price']
    list_display = ('created_at', 'id', 'user', 'total_price', 'address',
                    'contact', 'is_delivered')
    ordering = ('is_delivered', '-created_at',)
    date_hierarchy = 'created_at'

    # def has_delete_permission(self, request, obj=None):
    #     return False


admin.site.register(Order, OrderAdmin)
