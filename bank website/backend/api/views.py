from rest_framework import generics, status, permissions
from django.contrib.auth.models import User
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from decimal import Decimal, InvalidOperation
from django.db import transaction

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    transaction_number = request.data.get('transaction_number')
    receiver = request.data.get('receiver')
    extracted_amount = request.data.get('amount')

    try:
        extracted_amount = Decimal(extracted_amount)
    except InvalidOperation:
        return Response({'error': 'Invalid amount format'}, status=400)

    payment = Payment.objects.filter(
        payment_number=transaction_number,
        receiver__account_number=receiver,
        amount=extracted_amount
    ).first()

    if payment:
        return Response({
            'verified': True,
            'actual_amount': str(payment.amount),
            'extracted_amount': str(extracted_amount),
            'is_sufficient': extracted_amount >= payment.amount
        })
    else:
        return Response({'verified': False, 'error': 'Payment not found'})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = User.objects.get(id=token.user_id)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data,
        })
    

class LogoutView(APIView):
    def post(self, request):
        token = request.auth
        if token:
            token.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)    


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def verify_token(request):
    user = request.user
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
        }
    })


class BankAccountDetail(generics.RetrieveAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.bankaccount


class PaymentCreateView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        payer_account_number = request.data.get('payer')
        receiver_account_number = request.data.get('receiver')
        amount = request.data.get('amount')

        if not all([payer_account_number, receiver_account_number, amount]):
            return Response(
                {"error": "Payer, receiver, and amount are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = Decimal(amount)
        except (TypeError, InvalidOperation):
            return Response(
                {"error": "Invalid amount format"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                # Get accounts with lock
                payer_account = BankAccount.objects.select_for_update().get(
                    account_number=payer_account_number
                )
                receiver_account = BankAccount.objects.select_for_update().get(
                    account_number=receiver_account_number
                )

                # Check if user owns the payer account
                if payer_account.user != request.user:
                    return Response(
                        {"error": "You can only make payments from your own account"},
                        status=status.HTTP_403_FORBIDDEN
                    )

                # Check balance
                if payer_account.balance < amount:
                    return Response({
                        "error": "Insufficient funds",
                        "available_balance": str(payer_account.balance),
                        "required_amount": str(amount)
                    }, status=status.HTTP_400_BAD_REQUEST)

                # Prepare payment data
                payment_data = {
                    'payer': payer_account.id,
                    'receiver': receiver_account.id,
                    'amount': amount,
                    'description': request.data.get('description', 'Payment transaction')
                }

                serializer = self.get_serializer(data=payment_data)
                serializer.is_valid(raise_exception=True)

                # Update balances
                payer_account.balance -= amount
                receiver_account.balance += amount
                
                # Save everything
                payer_account.save()
                receiver_account.save()
                self.perform_create(serializer)

                # Prepare response
                response_data = serializer.data
                response_data['new_balance'] = str(payer_account.balance)
                
                return Response(response_data, status=status.HTTP_201_CREATED)

        except BankAccount.DoesNotExist:
            return Response(
                {"error": "Invalid account number"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class PaymentListView(generics.ListAPIView):
    # queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(payer__user=user) | Payment.objects.filter(receiver__user=user)
    
