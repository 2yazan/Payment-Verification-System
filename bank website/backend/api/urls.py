from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-token/', verify_token, name='verify_token'),
    path('account/', BankAccountDetail.as_view(), name='account'),
    path('payments/', PaymentListView.as_view(), name='payments_list'),
    # path('payments/<int:id>', PaymentListView.as_view(), name='payments_list'),
    path('payments/create/', PaymentCreateView.as_view(), name='payments_create'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),

]


