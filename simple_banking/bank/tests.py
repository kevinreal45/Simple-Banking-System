from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bank.models import Account, Transaction, Customer

class AccountTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            address="123 Main St",
            password="password123"
        )
        self.account = Account.objects.create(
            customer=self.customer,
            account_number="1234567890",
            account_type="Savings",
            balance=1000
        )

    def test_get_account_list(self):
        url = reverse('account-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_account_detail(self):
        url = reverse('account-detail', args=[self.account.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_account(self):
        url = reverse('account-list')
        data = {
            'customer': self.customer.id,
            'account_number': '0987654321',
            'account_type': 'Current',
            'balance': 500
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_account(self):
        url = reverse('account-detail', args=[self.account.id])
        data = {
            'customer': self.customer.id,
            'account_number': '1234567890',
            'account_type': 'Savings',
            'balance': 1500
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_account(self):
        url = reverse('account-detail', args=[self.account.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class TransactionTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            address="123 Main St",
            password="password123"
        )
        self.account = Account.objects.create(
            customer=self.customer,
            account_number="1234567890",
            account_type="Savings",
            balance=1000
        )
        self.transaction = Transaction.objects.create(
            account=self.account,
            amount=100,
            transaction_type='Deposit',
            balance_after_transaction=self.account.balance + 100
        )

    def test_get_transaction_list(self):
        url = reverse('transaction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_transaction_detail(self):
        url = reverse('transaction-detail', args=[self.transaction.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_transaction(self):
        url = reverse('transaction-list')
        data = {
            'account': self.account.id,
            'amount': 200,
            'transaction_type': 'Withdrawal',
            'balance_after_transaction': self.account.balance - 200
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_transaction(self):
        url = reverse('transaction-detail', args=[self.transaction.id])
        data = {
            'account': self.account.id,
            'amount': 150,
            'transaction_type': 'Withdrawal',
            'balance_after_transaction': self.account.balance - 150
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_transaction(self):
        url = reverse('transaction-detail', args=[self.transaction.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
