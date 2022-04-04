import django_filters as filters
from recipes.models import Recipe
from users.models import User


class RecipeFilter(filters.FilterSet):
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    tags = filters.AllValuesFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)

    def filter_is_favorited(self, queryset, name, value):
        pass

    def filter_is_in_shopping_cart(self, queryset, name, value):
        pass
