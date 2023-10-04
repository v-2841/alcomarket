from django.db import models


class Feedback(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Имя',
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
    )
    message = models.TextField(
        verbose_name='Сообщение',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время',
    )
    is_processed = models.BooleanField(
        default=False,
        verbose_name='Обработан',
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'

    def __str__(self):
        return self.name
