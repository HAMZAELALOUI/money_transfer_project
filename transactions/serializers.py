from rest_framework import serializers

from transactions.models import Transaction, TransactionFee


class TransactionFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionFee
        fields = ["id", "amount", "fee_type"]


class TransactionSerializer(serializers.ModelSerializer):
    fee = TransactionFeeSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "sender",
            "receiver",
            "agent",
            "amount",
            "currency",
            "status",
            "completed_at",
            "fee",
        ]
        read_only_fields = ["id", "status", "completed_at"]


class CreateTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["sender", "receiver", "amount", "currency"]
