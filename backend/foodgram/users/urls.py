from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet

app_name = 'api'
router = DefaultRouter()
# router.register(r'api/users/subscriptions', FollowViewSet, basename='follow')
router.register('users', CustomUserViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
