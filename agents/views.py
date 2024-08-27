from datetime import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Agent
from .serializers import AgentSerializer


class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

    @action(detail=True, methods=["post"])
    def payout(self, request, pk=None):
        agent = self.get_object()
        if agent.total_commission > 0:
            # In a real-world scenario, you'd integrate with a payment system here
            agent.last_payout = timezone.now()
            agent.total_commission = 0
            agent.save()
            return Response({"status": "payout successful"})
        return Response(
            {"status": "no commission to pay out"}, status=status.HTTP_400_BAD_REQUEST
        )
