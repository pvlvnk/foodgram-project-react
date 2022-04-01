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
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, author=obj).exists()


# class FollowSerializer(ModelSerializer):
#     following = serializers.SlugRelatedField(
#         slug_field='username',
#         queryset=User.objects.all()
#     )

#     class Meta:
#         model = Follow
#         fields = ('following',)
