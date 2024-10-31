from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import random
import string

class BankAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True, editable=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=500.00)
    account_holder_name = models.CharField(max_length=100)
    creation_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    def generate_account_number(self):
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        unique_id = ''.join(random.choices(string.digits, k=4))
        return timestamp[-6:] + unique_id
    
    def __str__(self):
        return f"{self.user.username}'s Account"

@receiver(post_save, sender=User)
def create_bank_account(sender, instance, created, **kwargs):
    if created:
        BankAccount.objects.create(
            user=instance,
            account_holder_name=instance.username
        )

class Payment(models.Model):
    payer = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='outgoing_payments')
    receiver = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name='incoming_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)
    payment_number = models.CharField(max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.payment_number:
            self.payment_number = self.generate_payment_number()
        super().save(*args, **kwargs)

    def generate_payment_number(self):
        while True:
            unique_number = ''.join(random.choices(string.digits, k=10))
            if not Payment.objects.filter(payment_number=unique_number).exists():
                return unique_number

    def __str__(self):
        return f"Payment from {self.payer} to {self.receiver}"
