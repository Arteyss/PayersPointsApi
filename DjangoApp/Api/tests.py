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
        self.transaction1 = Transaction.objects.create(payer='John', points=100)
        self.transaction2 = Transaction.objects.create(payer='Bob', points=50)
        self.points_to_spend_1 = {'points': 150}
        self.points_to_spend_2 = {'points': 80}

    def test_spend_points_api(self):
        """
        Test if spending points API is working
        """
        response = self.client.post(self.url, self.points_to_spend_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'payer': 'Bob', 'points': -50},
                                         {'payer': 'John', 'points': -100}])
        self.assertEqual(Transaction.objects.count(), 4)

        response = self.client.post(self.url, self.points_to_spend_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [{'payer': 'Bob', 'points': 0},
                                         {'payer': 'John', 'points': -80}])
        self.assertEqual(Transaction.objects.count(), 6)


class BalanceAPIViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('balance')
        self.transaction1 = Transaction.objects.create(payer='John', points=100)
        self.transaction2 = Transaction.objects.create(payer='Bob', points=5000)
        self.transaction3 = Transaction.objects.create(payer='John', points=200)
        self.transaction4 = Transaction.objects.create(payer='Bob', points=-100)

    def test_balance_api(self):
        """
        Test if balance API is working
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'John': 300, 'Bob': 4900})
