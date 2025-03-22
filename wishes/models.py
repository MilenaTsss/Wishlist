from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishes')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_reserved = models.BooleanField(default=False)
    reserved_by = models.ForeignKey(User, null=True, blank=False, on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
