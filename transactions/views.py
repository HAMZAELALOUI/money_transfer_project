from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Transaction
from .serializers import TransactionSerializer, CreateTransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTransactionSerializer
        return TransactionSerializer

    @action(detail=True, methods=["post"])
    def process(self, request, pk=None):
        transaction = self.get_object()
        if transaction.status == "PENDING":
            transaction.status = "PROCESSING"
            transaction.save()
            return Response({"status": "transaction processing"})
        return Response(
            {"status": "transaction cannot be processed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        transaction = self.get_object()
        if transaction.status == "PROCESSING":
            transaction.status = "COMPLETED"
            transaction.save()
            return Response({"status": "transaction completed"})
        return Response(
            {"status": "transaction cannot be completed"},
            status=status.HTTP_400_BAD_REQUEST,
        )
