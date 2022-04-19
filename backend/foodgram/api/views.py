from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram.settings import NAME_SHOPPING_CART_PDF
from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)
from users.serializers import RecipesBriefSerializer
from api.filters import RecipeFilter
from api.paginations import CustomPagination
from api.permissions import AuthorOrReadOnly
from api.serializers import (CartSerializer, FavoriteSerializer,
                             IngredientSerializer, ReadRecipeSerializer,
                             TagSerializer, WriteRecipeSerializer)

CONTENT_TYPE = 'application/pdf'


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Возвращает список всех ингредиентов или конкретный ингредиент."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Возвращает список всех тегов или конкретный тег."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Позволяет получить список всех рецептов, конкретный рецепт,
    создать/изменить/удалить свой рецепт.

    """
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    paginations_class = CustomPagination
    permission_classes = (AuthorOrReadOnly,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE'):
            return WriteRecipeSerializer
        return ReadRecipeSerializer

    def add_or_del_object(self, model, pk, serializer, errors):
        recipe = get_object_or_404(Recipe, id=pk)
        serializer = serializer(
            data={'user': self.request.user.id, 'recipe': recipe.id}
        )
        if self.request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = RecipesBriefSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        object = model.objects.filter(user=self.request.user, recipe=recipe)
        if not object.exists():
            return Response(
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def creating_pdf(dictionary, pdf_file):
        begin_position_x, begin_position_y = 30, 730
        pdfmetrics.registerFont(TTFont('TNR', 'times.ttf'))
        pdf_file.setFont('TNR', 25)
        pdf_file.setTitle('Список покупок')
        pdf_file.drawString(
            begin_position_x, begin_position_y + 40, 'Список покупок: ')
        pdf_file.setFont('TNR', 18)
        for number, item in enumerate(dictionary, start=1):
            if begin_position_y < 100:
                begin_position_y = 730
                pdf_file.showPage()
                pdf_file.setFont('TNR', 18)
            pdf_file.drawString(
                begin_position_x,
                begin_position_y,
                f'{number}: {item["ingredient__name"]} - '
                f'{item["ingredient_total"]}'
                f'{item["ingredient__measurement_unit"]}'
            )
            begin_position_y -= 30
        pdf_file.showPage()
        return pdf_file.save()

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        url_path='favorite',
        url_name='favorite',
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        errors = 'У вас нет данного рецепта в избранном'
        return self.add_or_del_object(Favorite, pk, FavoriteSerializer, errors)

    @action(
        detail=True,
        methods=('POST', 'DELETE'),
        url_path='shopping_cart',
        url_name='shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        errors = 'У вас нет данного рецепта в списке покупок'
        return self.add_or_del_object(Cart, pk, CartSerializer, errors)

    @action(
        detail=False,
        url_path='download_shopping_cart',
        url_name='download_shopping_cart',
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        ingredients = IngredientRecipe.objects.filter(
            recipe__carts__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(ingredient_total=Sum('amount'))

        response = HttpResponse(content_type=CONTENT_TYPE)
        response['Content-Disposition'] = (
            f'attachment; filename={NAME_SHOPPING_CART_PDF}')
        pdf_file = canvas.Canvas(response)
        self.creating_pdf(ingredients, pdf_file)
        return response


class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return recipe.favorites.all()
