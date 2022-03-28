from django.contrib import admin

from recipes.models import Ingredient, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'amount',
        'measurement_unit'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    list_editable = ('name',)
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    pass


class RecipeAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
