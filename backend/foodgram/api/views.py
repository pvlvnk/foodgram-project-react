from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from api.filters import RecipeFilter
from api.permissions import AuthorOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             ReadRecipeSerializer, TagSerializer,
                             WriteRecipeSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Возвращает список всех ингредиентов или конкретный ингредиент."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Возвращает список всех тегов или конкретный тег."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Позволяет получить список всех рецептов, конкретный рецепт,
    создать/изменить/удалить свой рецепт.

    """
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    paginations_class = PageNumberPagination
    # filterset_fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')
    filterset_class = RecipeFilter
    ordering_fields = ('-id',)

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
