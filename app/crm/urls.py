from django.urls import path
from . import views

urlpatterns = [
    path('payment_requests/', views.payment_request_view, name='payment_applications'),
    path('payment_requests_update/<int:application_id>/', views.payment_request_update_status_view, name='payment_status_update'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('tour_payments/', views.tour_payments_view, name='tour_payments')
]
