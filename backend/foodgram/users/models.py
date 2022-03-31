from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'username')
    username = models.CharField(
        unique=True,
        max_length=50,
        verbose_name='Имя пользователя',
        help_text='Введите юзернейм',
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='Имя',
        help_text='Введите имя',
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='Фамилия',
        help_text='Введите фамилию',
    )
    email = models.EmailField(
        max_length=50,
        blank=False,
        unique=True,
        verbose_name='Адрес электронной почты',
        help_text='Укажите адрес электронной почты',
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
