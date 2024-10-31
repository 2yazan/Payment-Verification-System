from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('insurance/', InsuranceList.as_view(), name='Insurance-list'),
    path('user-insurances/', UserInsuranceList.as_view(), name='user-insurance-list'),
    path('upload/payment-check/', upload_payment_check, name='upload_payment_check'),
    path('verify-payment/', views.verify_payment_with_bank, name='verify_payment'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-token/', verify_token, name='verify_token'),
]
