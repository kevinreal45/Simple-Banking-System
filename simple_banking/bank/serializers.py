from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Customer, Account, Transaction, Loan, User, Card

# Card Serializer
class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'account', 'card_number', 'card_type', 'expiry_date', 'is_active']

# Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'address', 'password', 'created_at', 'is_deleted', 'cards']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Hash the password before saving
        return super().create(validated_data)

# Account Serializer
class AccountSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    cards = CardSerializer(many=True, read_only=True)
    class Meta:
        model = Account
        fields = ['id', 'customer', 'account_number', 'account_type', 'balance', 'created_at', 'status', 'cards']

# Transaction Serializer
class TransactionSerializer(serializers.ModelSerializer):
    account = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all())
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'transaction_type', 'amount', 'transaction_date', 'description', 'balance_after_transaction']

# Loan Serializer
class LoanSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Loan
        fields = ['id', 'customer', 'loan_type', 'amount', 'interest_rate', 'loan_term_months', 'status', 'disbursed_date']

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'groups', 'user_permissions']

