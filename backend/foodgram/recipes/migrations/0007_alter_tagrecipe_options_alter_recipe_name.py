# Generated by Django 4.0.3 on 2022-04-02 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_favorite_favorite_favorite_unique'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tagrecipe',
            options={'verbose_name': 'Рецепты с тегами', 'verbose_name_plural': 'Рецепты с тегами'},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(help_text='Введите название рецепта', max_length=200, verbose_name='Название рецепта'),
        ),
    ]