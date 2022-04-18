from django.contrib import admin

from .models import (Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag,
                     TagRecipe)


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    empty_value_display = '-empty-'
    inlines = (IngredientRecipeInline,)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-empty-'
    inlines = (TagRecipeInline,)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name',)
    list_filter = ('tags',)
    search_fields = ('author__username',)
    empty_value_display = '-empty-'
    filter_vertical = ('tags',)
    inlines = (TagRecipeInline, IngredientRecipeInline,)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user',)
    search_filter = ('user__username',)
    empty_value_display = '-empty-'


class CartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user',)
    search_filter = ('user__username',)
    empty_value_display = '-empty-'


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Cart, CartAdmin)
