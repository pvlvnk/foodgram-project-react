from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название ингредиента',
        help_text='Введите название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=100,
        verbose_name='Единица измерения',
        help_text='Введите единицу измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Название тега',
        help_text='Укажите название тега',
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
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Укажите автора',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Введите название рецепта',
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
        blank=True,
    )
    text = models.CharField(
        max_length=1024,
        verbose_name='Текст',
        help_text='Введите текст',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        db_index=True,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
        help_text='Укажите ингредиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        db_index=True,
        through='TagRecipe',
        verbose_name='Тег',
        help_text='Укажите теги',
    )
    cooking_time = models.SmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления',
        validators=[MinValueValidator(
            1, message='Время приготовления должно быть больше 0')]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        help_text='Укажите количество',
        validators=[MinValueValidator(
            1, message='Количество ингредиентов должно быть больше 0')]
    )

    def __str__(self) -> str:
        return f'{self.ingredient} для {self.recipe}'


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Рецепты с тегами'
        verbose_name_plural = 'Рецепты с тегами'

    def __str__(self) -> str:
        return f'{self.tag} для {self.recipe}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Укажите пользователя',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
        help_text='Выберите рецепт',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='favorite_unique'),
        )
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'

    def __str__(self) -> str:
        return f'У {self.user.username} избран {self.recipe}'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь',
        help_text='Укажите пользователя',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт',
        help_text='Укажите текст',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='cart_unique'),
        )
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self) -> str:
        return f'{self.recipe} в списке у {self.user.username}'
