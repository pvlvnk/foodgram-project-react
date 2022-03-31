from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Follow


class FollowSerializer(ModelSerializer):
    author = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Follow
        fields = ('user', 'author',)
