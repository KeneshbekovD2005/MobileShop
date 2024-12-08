from django.urls import path
from . import views

app_name = 'payment_system'

urlpatterns = [
    path('payment-application-order/<int:payment_method_id>/<int:tour_id>/', views.payment_application_order_view, name='payment_application'),
    path('applications/', views.my_payment_application_view, name='applications')
]
