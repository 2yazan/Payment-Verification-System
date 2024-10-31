from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
# Create your models here.

class Insurance(models.Model):
    package_name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    coverage_limit = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='posters/', null=True, blank=True)

    def __str__(self):
        return self.package_name



class UserInsurance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_insurances')
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    payment_check = models.FileField(upload_to='payment_checks/')
    status = models.CharField(max_length=50, default="Pending")
    verification_response = models.JSONField(null=True, blank=True)  # Stores bank response

    def __str__(self):
        return f"{self.user.username} - {self.insurance.package_name} (Status: {self.status})"

    def save(self, *args, **kwargs):
        # insurance will expire after 1 year
        if not self.expiry_date:
            self.expiry_date = self.purchase_date + timedelta(days=365)
        super().save(*args, **kwargs)

