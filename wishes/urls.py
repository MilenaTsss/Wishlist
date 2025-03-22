from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WishViewSet

router = DefaultRouter()
router.register(r'wishes', WishViewSet, basename='wish')

urlpatterns = [
    path('', include(router.urls)),
]
