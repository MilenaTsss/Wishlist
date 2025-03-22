from django.urls import include, path
from rest_framework.routers import SimpleRouter

from wishes.views import WishViewSet

router = SimpleRouter()
router.register(r'wishes', WishViewSet, basename='wish')

urlpatterns = [
    path('', include(router.urls)),
]
