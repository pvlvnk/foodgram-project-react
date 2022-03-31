from recipes.models import Ingredient, Recipe, Tag
from rest_framework import viewsets

from api.serializers import (IngredientSerializer, RecipeSerializer,
                             TagSerialier)
from api.permissions import ReadOnly


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (ReadOnly,)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerialier
    permission_classes = (ReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
