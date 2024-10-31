from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics, filters, permissions, status
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import logging
import re
import fitz
from PIL import Image
import pytesseract
from .models import *
from .serializers import *
import requests
from django.conf import settings


logger = logging.getLogger(__name__)


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
   

class InsuranceList(generics.ListAPIView):
    serializer_class = InsuranceSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Insurance.objects.all()


class UserInsuranceList(generics.ListCreateAPIView):
    serializer_class = UserInsuranceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['insurance__package_name']

    def get_queryset(self):
        return UserInsurance.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def get_bank_api_token():
    """Obtains the bank API token for authentication."""
    login_url = f"{settings.BANK_API_URL}/api/login/"
    login_data = {
        'username': settings.BANK_API_USERNAME,
        'password': settings.BANK_API_PASSWORD
    }
    try:
        response = requests.post(login_url, json=login_data)
        response.raise_for_status()
        return response.json().get('token')
    except Exception as e:
        logger.error(f"Error obtaining bank API token: {e}")
        raise Exception("Failed to obtain token")


def verify_payment_with_bank(transaction_number, receiver, amount):
    """Verifies the payment with the bank using the extracted transaction number, receiver, and amount."""
    verify_url = f"{settings.BANK_API_URL}/api/verify-payment/"
    token = get_bank_api_token()
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'transaction_number': transaction_number,  # Use transaction_number as required by bank
        'receiver': receiver,
        'amount': amount
    }
    try:
        response = requests.post(verify_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error verifying payment with bank: {e}")
        return None


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def upload_payment_check(request):
    if request.method == 'POST':
        logger.info("Request received for upload_payment_check.")

        logger.error("An error occurred: %s", str(e)) 
        try:
            # Check if the user is authenticated
            if request.user.is_authenticated:
                logger.debug("Received POST request")
                uploaded_file = request.FILES.get('payment_check')
                package_id = request.POST.get('id')  # Package being purchased
                logger.debug(f"Uploaded file: {uploaded_file}, Package ID: {package_id}")

                if not uploaded_file or not package_id:
                    return JsonResponse({'error': 'File or package ID missing'}, status=400)

                # Save the file temporarily
                filepath = save_uploaded_file(uploaded_file)
                if not filepath:
                    return JsonResponse({'error': 'Invalid file format'}, status=400)

                # Extract text from the file
                text = extract_text_from_file(filepath)
                sender, amount, receiver, transaction_number = extract_sender_amount_receiver(text)
                delete_uploaded_file(filepath) 

                if not amount or not receiver or not transaction_number:
                    return JsonResponse({'error': 'Failed to extract all required data'}, status=400)

                # Verify payment with the bank
                verification_result = verify_payment_with_bank(transaction_number, receiver, amount)
                if verification_result is None:
                    return JsonResponse({'error': 'Bank verification failed'}, status=500)

                # Check for package validity and fetch package price
                insurance_package = get_insurance_package(package_id)
                if not insurance_package:
                    return JsonResponse({'error': 'Invalid insurance package'}, status=404)

                # Check amount sufficiency
                is_sufficient = float(amount) >= float(insurance_package.price)
                status = "Verified" if verification_result.get('verified') and is_sufficient else "Failed"

                # Create and save UserInsurance instance
                user_insurance = create_user_insurance(request.user, insurance_package, uploaded_file, status, verification_result)

                # Respond with result
                return JsonResponse({
                    'status': user_insurance.status,
                    'expiry_date': user_insurance.expiry_date,
                    'verification_response': verification_result,
                    'sufficient_funds': is_sufficient
                })
            else:
                return JsonResponse({'error': 'User not authenticated'}, status=403)

        except Exception as e:
            logger.error(f"Error in upload_payment_check: {e}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



def save_uploaded_file(uploaded_file):
    """Validates and saves the uploaded file, returning the file path."""
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
    if not uploaded_file.name.lower().endswith(tuple(allowed_extensions)):
        return None

    fs = FileSystemStorage()
    filename = fs.save(uploaded_file.name, uploaded_file)
    return fs.path(filename) 


def delete_uploaded_file(filepath):
    """Deletes the temporary file after processing."""
    fs = FileSystemStorage()
    fs.delete(filepath)


def extract_text_from_file(file_path):
    """Extracts text from a PDF or image file."""
    text = ""
    try:
        if file_path.endswith(".pdf"):
            logger.debug("Processing PDF file")
            with fitz.open(file_path) as pdf_file:
                for page in pdf_file:
                    text += page.get_text()
            logger.debug(f"Extracted text from PDF: {text}") 
        else:
            logger.debug("Processing image file")
            image = Image.open(file_path)
            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, lang='eng', config=custom_config)
            logger.debug(f"Extracted text from image: {text}")

        return text
    except Exception as e:
        logger.error(f"Error extracting text from file {file_path}: {e}")
        return ""


def extract_sender_amount_receiver(text):
    """Extracts sender, amount, receiver, and transaction number from the extracted text."""
    try:
        sender_pattern = r"SENDER:\s*(\d+)"
        receiver_pattern = r"RECEIVER:\s*(\d+)"
        transaction_pattern = r"TRANSACTION NUMBER:\s*(\d+)"
        amount_pattern = r"TRANSACTION AMOUNT:\s*\$([0-9]+(\.[0-9]{1,2})?)"

        sender = re.search(sender_pattern, text)
        receiver = re.search(receiver_pattern, text)
        transaction_number = re.search(transaction_pattern, text)
        amount = re.search(amount_pattern, text)

        return (
            sender.group(1) if sender else None,
            amount.group(1) if amount else None,
            receiver.group(1) if receiver else None,
            transaction_number.group(1) if transaction_number else None
        )
    except Exception as e:
        logger.error(f"Error extracting data from text: {e}")
        return None, None, None, None



def get_insurance_package(package_id):
    """Fetches the insurance package based on the provided ID."""
    try:
        return Insurance.objects.get(id=package_id)
    except Insurance.DoesNotExist:
        return None


def create_user_insurance(user, insurance_package, payment_check, status, verification_result):
    """Creates and saves a new UserInsurance record in the database."""
    user_insurance = UserInsurance(
        user=user,
        insurance=insurance_package,
        payment_check=payment_check,
        status=status,
        verification_response=verification_result,
        is_active=verification_result.get('verified') and (float(verification_result.get('actual_amount', 0)) >= float(insurance_package.price))
    )
    user_insurance.save()
    return user_insurance
