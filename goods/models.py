from collections.abc import Iterable
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Product(models.Model):
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
        upload_to='products/',
        verbose_name='Изображение',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Производитель',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    archived = models.BooleanField(
        default=False,
        verbose_name='Архивирован',
    )

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         return super().save(*args, **kwargs)
    #     new_instance = Product()
    #     for field in self._meta.fields:
    #         setattr(new_instance, field.name, getattr(self, field.name))
    #     new_instance.some_field = "новое значение"
    #     new_instance.pk = None
    #     result = new_instance.save()
    #     return result


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
    products = models.ManyToManyField(
        Product,
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
    product = models.ForeignKey(
        Product,
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
