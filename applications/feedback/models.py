from django.db import models


class FeedbackMessage(models.Model):
    """ Класс модели сообщения обратной связи. """
    full_name = models.CharField(
        verbose_name='ФИО',
        max_length=250,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=250,
    )
    message = models.TextField(
        verbose_name='Сообщение',
        max_length=1000,
    )
    sent_at = models.DateTimeField(
        verbose_name='Отправлено в',
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return f'{self.full_name} - {self.email}'
    
    class Meta:
        verbose_name = "Сообщение обратной связи"
        verbose_name_plural = "Сообщения обратной связи"
