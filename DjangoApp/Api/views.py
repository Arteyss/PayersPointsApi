from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Transaction
from .serializers import SpendPointsSerializer, TransactionSerializer
from .utils import get_balance, point_counter


class TransactionAPIView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class SpendPointsAPIView(generics.CreateAPIView):
    queryset = Transaction.objects.order_by('timestamp')
    serializer_class = SpendPointsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        points_to_spend = serializer.validated_data['points']
        spent_points_list = point_counter(self.get_queryset(), points_to_spend)
        return Response(spent_points_list, status=status.HTTP_200_OK)


class BalanceAPIView(APIView):
    def get(self, request):
        balance_dict = get_balance()
        return Response(balance_dict, status=status.HTTP_200_OK)
