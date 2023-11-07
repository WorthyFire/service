from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from django.utils.translation import gettext_lazy as _
from .models import DesignRequest, DesignCategory


class RegistrationForm(forms.Form):
    full_name = forms.CharField(label='ФИО', max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Ваше ФИО'}))
    username = forms.CharField(label='Логин (латиница и дефис)', max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'placeholder': 'example@example.com'}))
    password = forms.CharField(label='Пароль', max_length=30, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password_confirm = forms.CharField(label='Повторите пароль', max_length=30, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))
    agree_to_processing = forms.BooleanField(label='Согласие на обработку персональных данных', required=True)

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if not re.match(r'^[а-яёА-ЯЁ\s-]+$', full_name):
            raise ValidationError("ФИО может содержать только кириллические буквы, дефис и пробелы.")
        return full_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z-]+$', username):
            raise ValidationError("Логин может содержать только латиницу и дефис.")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким логином уже существует.")
        return username

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise ValidationError("Пароли не совпадают.")
        return password_confirm

class DesignCategoryForm(forms.ModelForm):
    class Meta:
        model = DesignCategory
        fields = ['name']
        labels = {
            'name': 'Название категории'
        }
class DesignRequestFilterForm(forms.Form):
    STATUS_CHOICES = (
        ('', 'Все'),
        ('Новая', 'Новая'),
        ('Принято в работу', 'Принято в работу'),
        ('Выполнено', 'Выполнено'),
    )

    status = forms.ChoiceField(label='Статус заявки', choices=STATUS_CHOICES, required=False)


class DesignRequestForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['title', 'description', 'category', 'room_image']

    def clean_room_image(self):
        max_file_size_bytes = 2 * 1024 * 1024
        room_image = self.cleaned_data.get('room_image')

        if room_image and room_image.size > max_file_size_bytes:
            max_file_size_mb = max_file_size_bytes / (1024 * 1024)  # Конвертация в мегабайты
            raise forms.ValidationError(
                _('Максимальный размер файла: %(max_size)s МБ.') % {'max_size': max_file_size_mb}, code='file_size')

        return room_image

class ChangeRequestStatusForm(forms.ModelForm):
    class Meta:
        model = DesignRequest
        fields = ['status', 'comment', 'design_image']

    STATUS_CHOICES = [
        ('Новая', 'Новая'),
        ('Принято в работу', 'Принято в работу'),
        ('Выполнено', 'Выполнено'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Статус')
    comment = forms.CharField(required=False, widget=forms.Textarea)
    design_image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Проверка статуса заявки и отключение редактирования статуса при необходимости
        if self.instance.status != 'Новая':
            self.fields['status'].widget.attrs['disabled'] = True

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')

        if status == 'Принято в работу':

            comment = cleaned_data.get('comment')
            if not comment:
                raise forms.ValidationError("Комментарий обязателен для статуса 'Принято в работу'.")

        elif status == 'Выполнено':

            design_image = cleaned_data.get('design_image')
            if not design_image:
                raise forms.ValidationError("Фотография дизайна обязательна для статуса 'Выполнено'.")

        return cleaned_data
