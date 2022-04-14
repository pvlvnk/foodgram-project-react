from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Follow, User
from users.serializers import FollowSerializer, ResponeSubscribeSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = PageNumberPagination

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_path='subscribe',
        url_name='subscribe',
        permission_classes=(IsAuthenticated,),
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        serializer = FollowSerializer(
            data={'user': user.id, 'author': author.id}
        )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = ResponeSubscribeSerializer(
                author, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        follow = get_object_or_404(Follow, user=user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        url_path='subscriptions',
        url_name='subscriptions',
        permission_classes=(IsAuthenticated,),
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = ResponeSubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

# class FollowViewSet(viewsets.ModelViewSet):
#     serializer_class = FollowSerializer

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.request.user.username)
#         return user.follower.all()

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
