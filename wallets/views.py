from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Wallet
from .serializers import WalletSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    @action(detail=True, methods=["post"])
    def deposit(self, request, pk=None):
        wallet = self.get_object()
        amount = request.data.get("amount")
        if amount:
            wallet.balance += float(amount)
            wallet.save()
            return Response({"status": "deposit successful"})
        return Response(
            {"status": "invalid amount"}, status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=["post"])
    def withdraw(self, request, pk=None):
        wallet = self.get_object()
        amount = request.data.get("amount")
        if amount and wallet.balance >= float(amount):
            wallet.balance -= float(amount)
            wallet.save()
            return Response({"status": "withdrawal successful"})
        return Response(
            {"status": "insufficient funds or invalid amount"},
            status=status.HTTP_400_BAD_REQUEST,
        )
