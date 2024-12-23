from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError

# Customer Model
class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    password = models.CharField(max_length=128)  # To store hashed passwords
    created_at = models.DateTimeField(default=now)
    is_deleted = models.BooleanField(default=False)  # Soft delete field

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def reactivate(self):
        self.is_deleted = False
        self.save()

    def total_balance(self):
        return sum(account.balance for account in self.accounts.all())

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

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="accounts")
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

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_date = models.DateTimeField(default=now)
    description = models.TextField(blank=True, null=True)
    balance_after_transaction = models.DecimalField(max_digits=15, decimal_places=2)

    def clean(self):
        if self.transaction_type == 'Withdrawal' and self.amount > self.account.balance:
            raise ValidationError("Insufficient funds for withdrawal.")
        if self.account.status != 'Active':
            raise ValidationError("Transactions can only be made on active accounts.")

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

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="loans")
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # Use Decimal for precision
    loan_term_months = models.IntegerField(help_text="Loan term in months")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    disbursed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Loan ({self.loan_type}) - {self.amount} for {self.customer}"

# Card Model
class Card(models.Model):
    CARD_TYPES = [
        ('Debit', 'Debit'),
        ('Credit', 'Credit'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Blocked', 'Blocked'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="cards")
    card_number = models.CharField(max_length=16, unique=True)
    card_type = models.CharField(max_length=10, choices=CARD_TYPES)
    expiry_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')

    def __str__(self):
        return f"{self.card_type} Card {self.card_number} ({self.status})"

# Admin/User Model
class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Resolve the reverse accessor conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",  # Custom related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",  # Custom related name
        blank=True
    )

    def __str__(self):
        return self.username
