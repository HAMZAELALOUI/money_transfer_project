import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from transactions.models import Transaction, TransactionFee
from wallets.services import WalletService, InsufficientFundsError

logger = logging.getLogger("money_transfer")


class TransactionService:
    @staticmethod
    def create_transaction(sender, receiver, amount, currency="USD", agent=None):
        with transaction.atomic():
            try:
                # Create the transaction record
                new_transaction = Transaction.objects.create(
                    sender=sender,
                    receiver=receiver,
                    agent=agent,
                    amount=amount,
                    currency=currency,
                    status="PENDING",
                )

                # Perform the transfer
                WalletService.transfer(sender, receiver, amount)

                # Update transaction status
                new_transaction.status = "COMPLETED"
                new_transaction.completed_at = timezone.now()
                new_transaction.save()

                logger.info(
                    f"Transaction created: {new_transaction.id} - {sender} to {receiver} - {amount} {currency}"
                )
                return new_transaction
            except InsufficientFundsError as e:
                logger.warning(
                    f"Transaction failed due to insufficient funds: {sender} to {receiver} - {amount} {currency}"
                )
                if new_transaction:
                    new_transaction.status = "FAILED"
                    new_transaction.save()
                raise
            except Exception as e:
                logger.error(
                    f"Transaction failed: {sender} to {receiver} - {amount} {currency}. Error: {str(e)}"
                )
                if new_transaction:
                    new_transaction.status = "FAILED"
                    new_transaction.save()
                raise

    @staticmethod
    def get_user_transactions(user):
        return Transaction.objects.filter(sender=user) | Transaction.objects.filter(
            receiver=user
        )

    @staticmethod
    def get_transaction_by_id(transaction_id):
        try:
            return Transaction.objects.get(id=transaction_id)
        except ObjectDoesNotExist:
            logger.warning(f"Transaction not found: {transaction_id}")
            return None

    @staticmethod
    def cancel_transaction(transaction_id):
        with transaction.atomic():
            try:
                trans = Transaction.objects.select_for_update().get(id=transaction_id)
                if trans.status != "COMPLETED":
                    raise ValueError("Only completed transactions can be cancelled")

                # Check if the transaction is not too old to be cancelled (e.g., within 24 hours)
                if (
                    trans.completed_at
                    and (timezone.now() - trans.completed_at).days >= 1
                ):
                    raise ValueError("Transaction is too old to be cancelled")

                # Reverse the transfer
                WalletService.transfer(trans.receiver, trans.sender, trans.amount)

                trans.status = "CANCELLED"
                trans.save()

                logger.info(f"Transaction cancelled: {trans.id}")
                return trans
            except ObjectDoesNotExist:
                logger.warning(
                    f"Attempted to cancel non-existent transaction: {transaction_id}"
                )
                raise ValueError("Transaction not found")
            except Exception as e:
                logger.error(
                    f"Transaction cancellation failed: {transaction_id}. Error: {str(e)}"
                )
                raise

    @staticmethod
    def get_transaction_status(transaction_id):
        try:
            trans = Transaction.objects.get(id=transaction_id)
            return trans.status
        except ObjectDoesNotExist:
            logger.warning(
                f"Attempted to get status of non-existent transaction: {transaction_id}"
            )
            return None

    @staticmethod
    def add_transaction_fee(transaction, fee_amount, fee_type):
        try:
            fee = TransactionFee.objects.create(
                transaction=transaction, amount=fee_amount, fee_type=fee_type
            )
            logger.info(
                f"Fee added to transaction {transaction.id}: {fee_amount} {fee_type}"
            )
            return fee
        except Exception as e:
            logger.error(
                f"Failed to add fee to transaction {transaction.id}. Error: {str(e)}"
            )
            raise

    @staticmethod
    def get_agent_transactions(agent):
        return Transaction.objects.filter(agent=agent)
