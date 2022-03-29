from recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets

from api.serializers import (IngredientSerializer, RecipeSerializer,
                             TagSerialier)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerialier


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
