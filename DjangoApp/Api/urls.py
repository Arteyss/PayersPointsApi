from django.urls import path

from .views import BalanceAPIView, SpendPointsAPIView, TransactionAPIView

urlpatterns = [
    path('transactions/', TransactionAPIView.as_view(), name='transaction-list-create'),
    path('spend-points/', SpendPointsAPIView.as_view(), name='spend-points'),
    path('balance/', BalanceAPIView.as_view(), name='balance'),
]
