from django.contrib import admin

from payment_system.models import PaymentMethod, ProductPaymentApplication

# Register your models here.
admin.site.register(PaymentMethod)
admin.site.register(ProductPaymentApplication)