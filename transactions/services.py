from django.db import transaction

from transactions.models import Transaction
from wallets.services import WalletService


class TransactionService:
    @staticmethod
    def create_transaction(sender, receiver, amount, currency="USD"):
        with transaction.atomic():
            # Perform the transfer
            WalletService.transfer(sender, receiver, amount)

            # Create and save the transaction record
            new_transaction = Transaction.objects.create(
                sender=sender,
                receiver=receiver,
                amount=amount,
                currency=currency,
                status="COMPLETED",
            )

        return new_transaction

    @staticmethod
    def get_user_transactions(user):
        return Transaction.objects.filter(sender=user) | Transaction.objects.filter(
            receiver=user
        )

    @staticmethod
    def get_transaction_by_id(transaction_id):
        return Transaction.objects.filter(id=transaction_id).first()

    @staticmethod
    def cancel_transaction(transaction_id):
        with transaction.atomic():
            trans = Transaction.objects.select_for_update().get(id=transaction_id)
            if trans.status != "COMPLETED":
                raise ValueError("Only completed transactions can be cancelled")

            # Reverse the transfer
            WalletService.transfer(trans.receiver, trans.sender, trans.amount)

            trans.status = "CANCELLED"
            trans.save()

        return trans
