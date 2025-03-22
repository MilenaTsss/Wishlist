from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from wishes.models import Wish
from wishes.serializers import WishSerializer

@permission_classes([IsAuthenticated])
class WishViewSet(viewsets.ModelViewSet):
    serializer_class = WishSerializer

    def get_queryset(self):
        return Wish.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
