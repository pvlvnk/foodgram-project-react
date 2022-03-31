from django.contrib import admin

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Tag, TagRecipe)


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    empty_value_display = '-empty-'
    inlines = (IngredientRecipeInline,)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-empty-'
    inlines = (TagRecipeInline,)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name',)
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = '-empty-'
    filter_vertical = ('tags',)
    inlines = (TagRecipeInline, IngredientRecipeInline,)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user',)
    list_filter = ('recipe', 'user',)
    empty_value_display = '-empty-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
