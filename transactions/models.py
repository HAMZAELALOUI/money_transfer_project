from django.db import models
from users.models import User
from utils.models import BaseModel


class Transaction(BaseModel):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    ]

    sender = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="sent_transactions"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="received_transactions"
    )
    agent = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="processed_transactions",
        null=True,
        blank=True,
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Transaction {self.id}: {self.sender} to {self.receiver} - {self.amount} {self.currency}"


class TransactionFee(BaseModel):
    transaction = models.OneToOneField(
        Transaction, on_delete=models.CASCADE, related_name="fee"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    fee_type = models.CharField(max_length=20)

    def __str__(self):
        return f"Fee for Transaction {self.transaction.id}: {self.amount} {self.transaction.currency}"
