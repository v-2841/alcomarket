from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from goods.models import Good


ORDER_STATUS = [
    ('1_PENDING', 'Ожидание'),
    ('2_PROCESSING', 'Обработка'),
    ('3_SHIPPED', 'Отправлен'),
    ('4_DELIVERED', 'Доставлен'),
    ('5_CANCELLED', 'Отменён'),
]
User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='orders',
    )
    goods = models.ManyToManyField(
        Good,
        through='OrderGood',
        verbose_name='Товары',
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal(0.00),
        verbose_name='Итого',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    address = models.TextField(
        max_length=1000,
        verbose_name='Адрес',
    )
    contact = models.CharField(
        max_length=64,
        verbose_name='Контактные данные',
    )
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS,
        default='1_PENDING',
        verbose_name='Статус',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.created_at.strftime("%c")} - Заказ №{self.id}'


@receiver(post_save, sender=Order)
def return_goods_after_cancelling(sender, instance, **kwargs):
    if instance.status == '5_CANCELLED':
        for order_good in instance.ordergood_set.all():
            order_good.good.stock += order_good.quantity
            order_good.good.save()


class OrderGood(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        verbose_name='Заказ',
    )
    good = models.ForeignKey(
        Good,
        on_delete=models.CASCADE,
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена, 1 шт.',
    )

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'

    def __str__(self):
        return f'{self.good.name} - Заказ №{self.order.id}'


@receiver(pre_save, sender=OrderGood)
def subtract_add_total_price(sender, instance, **kwargs):
    if instance.pk:
        old_order_good = OrderGood.objects.get(id=instance.id)
        order = instance.order
        order.total_price -= old_order_good.price * old_order_good.quantity
        order.save()


@receiver(post_save, sender=OrderGood)
def add_total_price(sender, instance, **kwargs):
    order = instance.order
    order.total_price += instance.price * instance.quantity
    order.save()


@receiver(post_delete, sender=OrderGood)
def subtract_total_price(sender, instance, **kwargs):
    order = instance.order
    order.total_price -= instance.price * instance.quantity
    order.save()
