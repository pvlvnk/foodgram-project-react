from urllib import request
from rest_framework.serializers import ModelSerializer
from recipes.models import Ingredient, Tag, Recipe, IngredientRecipe
from rest_framework import serializers


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagSerialier(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class RecipeSerializer(ModelSerializer):
    author = serializers.StringRelatedField
    tags = TagSerialier(many=True, required=True)
    ingredients = IngredientSerializer(many=True, required=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'name', 'image',
                  'text', 'cooking_time', 'is_favorited',
                  'is_in_shopping_cart',)

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            amount = ingredient.get('amount')
            current_ingredient = Ingredient.objects.get_or_create(**ingredient)
            IngredientRecipe.objects.create(
                ingredient=current_ingredient,
                amount=amount,
                recipe=recipe,
            )
        recipe.save()
        return recipe
