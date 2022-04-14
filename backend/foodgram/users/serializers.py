from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Follow, User


class UserSerializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed',)

    def get_is_subscribed(self, obj):
        print(obj)
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


class FollowSerializer(serializers.ModelSerializer):
    author = UserSerializer
    user = UserSerializer

    class Meta:
        model = Follow
        fields = ('author', 'user')

    def validate(self, data):
        author = data.get('author')
        user = data.get('user')
        if user == author:
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписаться на самого себя'}
            )
        elif Follow.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                {'errors': 'Вы уже подписаны на данного пользователя'}
            )

    def create(self, validated_data):
        author = validated_data.get('author')
        user = validated_data.get('user')
        return Follow.objects.create(user=user, author=author)


class RecipesForSubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ResponeSubscribeSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.POST.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj)
        if recipes_limit:
            queryset = queryset[:(recipes_limit)]
        return RecipesForSubscribeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
