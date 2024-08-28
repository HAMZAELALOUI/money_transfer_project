from decimal import Decimal
from django.db import transaction

from wallets.models import Wallet


class InsufficientFundsError(Exception):
    pass


class WalletService:
    @staticmethod
    def get_balance(user):
        wallet = Wallet.objects.get(user=user)
        return wallet.balance

    @staticmethod
    def deposit(user, amount):
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=user)
            wallet.balance += Decimal(amount)
            wallet.save()
        return wallet

    @staticmethod
    def withdraw(user, amount):
        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(user=user)
            if wallet.balance < Decimal(amount):
                raise InsufficientFundsError("Insufficient funds for withdrawal")
            wallet.balance -= Decimal(amount)
            wallet.save()
        return wallet

    @staticmethod
    def transfer(from_user, to_user, amount):
        with transaction.atomic():
            from_wallet = Wallet.objects.select_for_update().get(user=from_user)
            to_wallet = Wallet.objects.select_for_update().get(user=to_user)

            if from_wallet.balance < Decimal(amount):
                raise InsufficientFundsError("Insufficient funds for transfer")

            from_wallet.balance -= Decimal(amount)
            to_wallet.balance += Decimal(amount)

            from_wallet.save()
            to_wallet.save()

        return from_wallet, to_wallet
