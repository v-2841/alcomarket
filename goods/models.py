from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Good(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
    )
    stock = models.PositiveIntegerField(
        verbose_name='Наличие на складе',
    )
    image = models.ImageField(
        upload_to='goods/',
        verbose_name='Изображение',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Категория',
    )
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Производитель',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Активный',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            return super(Good, self).save(*args, **kwargs)
        good = Good.objects.get(id=self.id)
        if good.price != self.price:
            good.active = False
            super(Good, good).save(*args, **kwargs)
            self.id = None
            self._state.adding = True
            return super(Good, self).save(*args, **kwargs)
        return super(Good, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise Exception('Нельзя удалять товары. Отмечайте их как архивные.')


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование категории',
    )

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование производителя',
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    goods = models.ManyToManyField(
        Good,
        through='OrderItem',
        verbose_name='Товары',
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Итоговая цена',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )


class OrderItem(models.Model):
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
        verbose_name='Цена',
    )
