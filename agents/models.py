from django.db import models
from utils.models import BaseModel
from users.models import User


class Agent(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2)
    total_commission = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    last_payout = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Agent: {self.user.username}"
