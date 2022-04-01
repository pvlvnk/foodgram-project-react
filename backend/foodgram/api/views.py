from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets

from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             ReadRecipeSerializer, TagSerializer,
                             WriteRecipeSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            return WriteRecipeSerializer
        return ReadRecipeSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return recipe.favorites.all()
