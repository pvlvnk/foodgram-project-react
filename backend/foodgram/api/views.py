from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import Favorite
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializers import RecipesBriefSerializer

from api.filters import RecipeFilter
from api.paginations import CustomPagination
# from api.permissions import AuthorOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             ReadRecipeSerializer, TagSerializer,
                             WriteRecipeSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Возвращает список всех ингредиентов или конкретный ингредиент."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
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
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    paginations_class = CustomPagination
    filterset_class = RecipeFilter
    ordering_fields = ('-id',)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH', 'DELETE']:
            return WriteRecipeSerializer
        return ReadRecipeSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='favorite',
        url_name='favorite',
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = FavoriteSerializer(
            data={'user': request.user.id, 'recipe': recipe.id}
        )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = RecipesBriefSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = Favorite.objects.filter(user=request.user, recipe=recipe)
        if not favorite.exists():
            return Response(
                {'errors': 'У вас нет данного рецепта в избранном'},
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return recipe.favorites.all()
