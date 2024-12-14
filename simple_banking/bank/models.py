from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser

# Customer Model
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=128)  # To store hashed passwords
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Account Model
class Account(models.Model):
    ACCOUNT_TYPES = [
        ('Savings', 'Savings'),
        ('Current', 'Current'),
        ('Fixed Deposit', 'Fixed Deposit'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Closed', 'Closed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"Account {self.account_number} ({self.account_type})"


# Transaction Model
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
        ('Transfer', 'Transfer'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateTimeField(default=now)
    description = models.TextField(blank=True, null=True)
    balance_after_transaction = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.transaction_date}"


# Loan Model
class Loan(models.Model):
    LOAN_TYPES = [
        ('Personal', 'Personal'),
        ('Mortgage', 'Mortgage'),
        ('Business', 'Business'),
    ]
    STATUS_CHOICES = [
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
        ('Closed', 'Closed'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.FloatField()
    loan_term = models.IntegerField(help_text="Loan term in months")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    disbursed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Loan ({self.loan_type}) - {self.amount} for {self.customer}"


# Admin/User Model
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
