from rest_framework import serializers

from .models import Wish


class WishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wish
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
