from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


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


@receiver(post_save, sender=Good)
def update_active_status(sender, instance, **kwargs):
    if instance.stock == 0 and instance.active:
        instance.active = False
        instance.save()


@receiver(pre_save, sender=Good)
def check_price_change(sender, instance, **kwargs):
    if instance.pk is not None:
        previous_good = Good.objects.get(pk=instance.pk)
        if previous_good.price != instance.price:
            instance.shopping_carts.all().delete()


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

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'good'], name='already_in_shopping_cart'),
        ]

    def __str__(self):
        return self.user.username + ' - ' + self.good.name


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Наименование категории',
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

    class Meta:
        ordering = ('name',)
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name
