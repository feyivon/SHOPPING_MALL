from django.contrib.auth.models import User
from django.db import models

# Product model
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name

# SavedCart model
class SavedCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cart_data = models.JSONField()
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.username} saved at {self.saved_at}"
        else:
            return f"Cart saved at {self.saved_at} (no user)"