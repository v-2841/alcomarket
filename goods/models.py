from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse


User = get_user_model()


class Good(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Наименование',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
    )
    volume = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        verbose_name='Объем, л',
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
        related_name='goods',
        verbose_name='Категория',
    )
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='goods',
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
    purchase_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Число проданных товаров',
    )
    is_in_shopping_cart = models.ManyToManyField(
        User,
        through='UserShoppingCart',
        related_name='shopping_cart',
        verbose_name='В корзине',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        raise Exception('Нельзя удалять товары. Отмечайте их как архивные.')

    def get_absolute_url(self):
        return reverse('goods:good_detail', kwargs={'good_id': self.id})


@receiver(pre_save, sender=Good)
def check_price_change(sender, instance, **kwargs):
    if instance.pk is not None:
        previous_good = Good.objects.get(pk=instance.pk)
        if previous_good.price != instance.price:
            instance.shopping_carts.all().delete()


@receiver(post_save, sender=Good)
def update_shopping_carts(sender, instance, **kwargs):
    good_in_shopping_carts = instance.shopping_carts.all()
    if instance.stock == 0:
        good_in_shopping_carts.delete()
    for shopping_cart in good_in_shopping_carts:
        if instance.stock < shopping_cart.quantity:
            shopping_cart.quantity = instance.stock
            shopping_cart.save()


class UserShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    good = models.ForeignKey(
        Good,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Товар',
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'good'], name='already_in_shopping_cart'),
        ]

    def __str__(self):
        return self.user.username + ' - ' + self.good.name

    def clean(self):
        if self.quantity > self.good.stock:
            raise ValidationError(
                {'quantity': 'На складе нет такого количества товаров'})


@receiver(post_save, sender=UserShoppingCart)
def check_quantity(sender, instance, **kwargs):
    if instance.quantity == 0:
        instance.delete()


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование производителя',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name
