from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from users.models import Follow, User
# from users.serializers import FollowSerializer


# class FollowViewSet(viewsets.ModelViewSet):
#     serializer_class = FollowSerializer

#     def get_queryset(self):
#         user = get_object_or_404(User, username=self.request.user.username)
#         return user.follower.all()

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
