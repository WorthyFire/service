from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class CustomUser(models.Model):
    full_name = models.CharField(max_length=255)
    consent_to_process_data = models.BooleanField(default=False)

class DesignCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class DesignRequest(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(DesignCategory, on_delete=models.CASCADE, verbose_name='Категория')
    room_image = models.ImageField(
        upload_to='design_images/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])],
        verbose_name='Фото помещения или план'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.CharField(max_length=20, default="Новая", verbose_name='Статус')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    def __str__(self):
        return self.title