from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from transactions.models import Transaction
from transactions.permissions import IsInvolvedOrAdmin
from transactions.serializers import CreateTransactionSerializer, TransactionSerializer
from transactions.services import TransactionService
from wallets.services import InsufficientFundsError


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsInvolvedOrAdmin]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTransactionSerializer
        return TransactionSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            transaction = TransactionService.create_transaction(
                sender=serializer.validated_data["sender"],
                receiver=serializer.validated_data["receiver"],
                amount=serializer.validated_data["amount"],
                currency=serializer.validated_data.get("currency", "USD"),
            )
            return Response(
                TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED
            )
        except InsufficientFundsError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        try:
            cancelled_transaction = TransactionService.cancel_transaction(pk)
            return Response(TransactionSerializer(cancelled_transaction).data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def user_transactions(self, request):
        user = request.user  # Assuming you're using authentication
        transactions = TransactionService.get_user_transactions(user)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def user_transactions(self, request):
        transactions = TransactionService.get_user_transactions(request.user)
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
