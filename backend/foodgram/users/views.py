from backend.foodgram.users.models import Follow
from rest_framework import viewsets
from backend.foodgram.users.serializers import FollowSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer