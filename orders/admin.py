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


@admin.action(description='Отметить как ожидающие')
def set_pending(self, request, queryset):
    queryset.update(status='1_PENDING')


@admin.action(description='Отметить как обрабатываемые')
def set_processing(self, request, queryset):
    queryset.update(status='2_PROCESSING')


@admin.action(description='Отметить как отправленные')
def set_shipped(self, request, queryset):
    queryset.update(status='3_SHIPPED')


@admin.action(description='Отметить как доставленные')
def set_delivered(self, request, queryset):
    queryset.update(status='4_DELIVERED')


@admin.action(description='Отметить как отменённые')
def set_cancelled(self, request, queryset):
    queryset.update(status='5_CANCELLED')


class OrderAdmin(admin.ModelAdmin):
    actions = [
        set_pending,
        set_processing,
        set_shipped,
        set_delivered,
        set_cancelled,
    ]
    inlines = [GoodInline]
    readonly_fields = ['user', 'user_full_name', 'total_price']
    list_display = ('created_at', 'id', 'user', 'user_full_name',
                    'total_price', 'address', 'contact', 'status')
    ordering = ('status', '-created_at',)
    date_hierarchy = 'created_at'

    def user_full_name(self, obj):
        return obj.user.get_full_name()

    def has_delete_permission(self, request, obj=None):
        return False

    user_full_name.short_description = 'Полное имя'


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderGood)
