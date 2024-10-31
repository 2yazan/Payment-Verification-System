from django.contrib import admin
from .models import *
# Register your models here.


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_number', 'balance', 'account_holder_name', 'creation_date')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payer', 'receiver', 'amount', 'description', 'date_time', 'payment_number')

admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Payment, PaymentAdmin)