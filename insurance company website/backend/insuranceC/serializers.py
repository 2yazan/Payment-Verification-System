from rest_framework import serializers
from .models import Insurance, UserInsurance
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user
    

class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        # fields = ['package_name', 'price', 'coverage_limit', 'description', 'cover']
        fields = '__all__'

class UserInsuranceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    insurance = InsuranceSerializer(read_only=True)

    class Meta:
        model = UserInsurance
        fields = [
            'id', 'user', 'insurance', 'purchase_date', 'expiry_date', 'is_active', 
            'status', 'payment_check', 'verification_response'
        ]
        read_only_fields = ['purchase_date', 'expiry_date', 'is_active', 'status', 'verification_response']