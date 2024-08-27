from rest_framework import serializers
from .models import Agent


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ["id", "user", "commission_rate", "total_commission", "last_payout"]
        read_only_fields = ["id", "total_commission", "last_payout"]
