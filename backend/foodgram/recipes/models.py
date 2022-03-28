from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название ингредиент',
        help_text='Введите название ингредиента',
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        help_text='Укажите количество',
    )
    measurement_unit = models.CharField(
        max_length=100,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент',
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    title = models.CharField(
        max_length=100,
        unique=True,
    )
    color = ColorField(
        unique=True,
        verbose_name='Цвет в HEX',
        help_text='Укажите цвет в HEX',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Уникальная строка',
        help_text='Введите уникальную строку',
    )

    class Meta:
        verbose_name = 'Тэг',
        verbose_name_plural = 'Тэги',

    def __str__(self) -> str:
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Укажите автора',
    )
    title = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Введите название',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
        blank=True,
    )
    text = models.CharField(
        verbose_name='Текст',
        help_text='Введите текст',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        db_index=True,
        # on_delete=models.SET_NULL,
        verbose_name='Ингредиенты',
        help_text='Укажите ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        # on_delete=models.SET_NULL,
        verbose_name='Тэг',
        help_text='Укажите тэги',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления',
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.title
