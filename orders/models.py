from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Sum

from goods.models import Good


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
    is_delivered = models.BooleanField(
        default=False,
        verbose_name='Доставлен',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.created_at.strftime("%c")} - Заказ №{self.id}'

    @property
    def total_price(self):
        total = self.ordergood_set.aggregate(total_price=Sum(
            F('price') * F('quantity'), output_field=models.DecimalField(
                max_digits=10, decimal_places=2)))['total_price']
        return total if total is not None else 0

    total_price.fget.short_description = 'Сумма'


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
