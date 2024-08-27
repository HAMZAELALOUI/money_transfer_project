from django.db import models
from utils.models import BaseModel
from users.models import User


class Wallet(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="USD")

    def __str__(self):
        return f"{self.user.username}'s Wallet: {self.balance} {self.currency}"
