from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.permissions import IsOwnerOrAdmin
from wallets.models import Wallet
from wallets.serializers import WalletSerializer
from wallets.services import InsufficientFundsError, WalletService


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsOwnerOrAdmin]

    @action(detail=True, methods=["post"])
    def deposit(self, request, pk=None):
        wallet = self.get_object()
        amount = request.data.get("amount")
        try:
            updated_wallet = WalletService.deposit(wallet.user, amount)
            return Response(WalletSerializer(updated_wallet).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def withdraw(self, request, pk=None):
        wallet = self.get_object()
        amount = request.data.get("amount")
        try:
            updated_wallet = WalletService.withdraw(wallet.user, amount)
            return Response(WalletSerializer(updated_wallet).data)
        except InsufficientFundsError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
