from backend.foodgram.api.serializers import (IngredientSerializer,
                                              RecipeSerializer, TagSerialier)
from backend.foodgram.recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerialier


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
