from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Transaction
from .serializers import TransactionSerializer


class TransactionAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('transaction-list-create')
        self.transaction_data = {'payer': 'John', 'points': 100}

    def test_transaction_create_api(self):
        """
        Test if transaction is created successfully through API
        """
        response = self.client.post(self.url, self.transaction_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().payer, 'John')

    def test_transaction_list_api(self):
        """
        Test if transaction list API is working
        """
        Transaction.objects.create(payer='John', points=100)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['payer'], 'John')

    def test_transaction_serializer(self):
        """
        Test if transaction serializer is working correctly
        """

        transaction = Transaction.objects.create(payer='John', points=100)
        serializer_data = {'payer': 'John', 'points': 100}
        serializer = TransactionSerializer(instance=transaction, data=serializer_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, serializer_data)


class SpendPointsAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('spend-points')
        self.transaction1 = Transaction.objects.create(payer='DANNON', points=300)
        self.transaction2 = Transaction.objects.create(payer='UNILEVER', points=200)
        self.transaction3 = Transaction.objects.create(payer='DANNON', points=-200)
        self.transaction4 = Transaction.objects.create(payer='MILLER COORS', points=10000)
        self.transaction5 = Transaction.objects.create(payer='DANNON', points=1000)
        self.points_to_spend_1 = {'points': 5000}
        self.points_to_spend_2 = {'points': 6300}
        self.points_to_spend_3 = {'points': 100}

    def test_spend_points_api(self):
        """
        Test if spending points API is working
        """
        response = self.client.post(self.url, self.points_to_spend_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'payer': 'DANNON', 'points': -100},
                                         {'payer': 'MILLER COORS', 'points': -4700},
                                         {'payer': 'UNILEVER', 'points': -200}])
        self.assertEqual(Transaction.objects.count(), 8)

        response = self.client.post(self.url, self.points_to_spend_2)
        self.assertEqual(response.data, [{'payer': 'DANNON', 'points': -1000},
                                         {'payer': 'MILLER COORS', 'points': -5300},
                                         {'payer': 'UNILEVER', 'points': 0}])
        self.assertEqual(Transaction.objects.count(), 10)

        response = self.client.post(self.url, self.points_to_spend_3)
        self.assertEqual(response.data, [{'payer': 'DANNON', 'points': 0},
                                         {'payer': 'MILLER COORS', 'points': 0},
                                         {'payer': 'UNILEVER', 'points': 0}])
        self.assertEqual(Transaction.objects.count(), 10)


class BalanceAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('balance')
        self.transaction1 = Transaction.objects.create(payer='DANNON', points=300)
        self.transaction2 = Transaction.objects.create(payer='UNILEVER', points=200)
        self.transaction3 = Transaction.objects.create(payer='DANNON', points=-200)
        self.transaction4 = Transaction.objects.create(payer='MILLER COORS', points=10000)
        self.transaction5 = Transaction.objects.create(payer='DANNON', points=1000)

    def test_balance_api(self):
        """
        Test if balance API is working
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'DANNON': 1100, 'MILLER COORS': 10000, 'UNILEVER': 200})
