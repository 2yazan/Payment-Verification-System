from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
import logging
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user
    

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    payer_account_number = serializers.SerializerMethodField()
    receiver_account_number = serializers.SerializerMethodField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Payment
        fields = ['id', 'amount', 'description', 'date_time', 'payer', 'receiver', 'payment_number',
                 'payer_account_number', 'receiver_account_number']
        read_only_fields = ['date_time']

    def get_payer_account_number(self, obj):
        return obj.payer.account_number

    def get_receiver_account_number(self, obj):
        return obj.receiver.account_number

    def validate(self, data):
        payer = data.get('payer')
        amount = data.get('amount')
        
        if not payer or not amount:
            raise serializers.ValidationError("Payer and amount are required")

        # Check if payer has sufficient balance
        if payer.balance < amount:
            raise serializers.ValidationError(
                f"Insufficient funds. Available balance: {payer.balance}, Required: {amount}"
            )
        return data
