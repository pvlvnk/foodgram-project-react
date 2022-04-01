from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            Tag)
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.serializers import UserSerializer


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientRecipeSerializer(ModelSerializer):
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class ReadRecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeSerializer(
        many=True,
        source='ingredientrecipe_set',
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image',
                  'text', 'cooking_time',)

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(user=request.user, recipe=obj).exists()


class WriteRecipeSerializer(ModelSerializer):
    ingredients = IngredientRecipeSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image', 'name', 'text',
                  'cooking_time')

    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            amount = ingredient.get('amount')
            base_ingredient = get_object_or_404(
                Ingredient, pk=ingredient.get('id'))
            IngredientRecipe.objects.create(
                recipe=recipe, ingredient=base_ingredient, amount=amount)
        return recipe


# class RecipeSerializer(ModelSerializer):
#     author = UserSerializer()
#     tags = TagSerialier(many=True, required=True)
#     ingredients = IngredientRecipeSerializer(
#         many=True,
#         required=True,
#         source='ingredientrecipe_set',
#     )
#     image = Base64ImageField()
#     is_favorited = serializers.SerializerMethodField()
#     is_in_shopping_cart = serializers.SerializerMethodField()

#     class Meta:
#         model = Recipe
#         fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
#                   'is_in_shopping_cart', 'name', 'image',
#                   'text', 'cooking_time',)

#     def create(self, validated_data):
#         tags = validated_data.pop('tags')
#         image = validated_data.pop('image')
#         ingredients = validated_data.pop('ingredients')
#         recipe = Recipe.objects.create(image=image, **validated_data)
#         recipe.tags.set(tags)
#         for ingredient in ingredients:
#             amount = ingredient.get('amount')
#             current_ingredient = Ingredient.objects.get_or_create(**ingredient)
#             IngredientRecipe.objects.create(
#                 ingredient=current_ingredient,
#                 amount=amount,
#                 recipe=recipe,
#             )
#         recipe.save()
#         return recipe

#     def get_is_favorited(self, obj):
#         request = self.context.get('request')
#         if request is None or request.user.is_anonymous:
#             return False
#         return Favorite.objects.filter(user=request.user, recipe=obj).exists()

#     def get_is_in_shopping_cart(self, obj):
#         request = self.context.get('request')
#         if request is None or request.user.is_anonymous:
#             return False
#         return Favorite.objects.filter(user=request.user, recipe=obj).exists()


# class ReadRecipeSerializer(ModelSerializer):
#     tags = TagSerialier(read_only=True, many=True)
#     author = UserSerializer(read_only=True)
#     ingredients =


class FavoriteSerializer(ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('id',)
