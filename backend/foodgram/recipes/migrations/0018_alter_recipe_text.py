# Generated by Django 4.0.4 on 2022-04-19 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0017_alter_ingredient_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.CharField(help_text='Введите текст', max_length=6144, verbose_name='Текст'),
        ),
    ]