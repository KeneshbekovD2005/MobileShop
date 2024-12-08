from django.contrib.auth import get_user_model
from django.db import models
from goods.models import Products
from payment_system.choices import PaymentApplicationStatusEnum
from user.models import MyUser

User = get_user_model()


class PaymentMethod(models.Model):
    title = models.CharField(max_length=35)
    logo = models.ImageField(upload_to='media/payment_methods_logo')
    qr = models.ImageField(upload_to='media/payment_methods_qr')
    personal_account = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cпособ оплаты'
        verbose_name_plural = 'Способы оплаты'


class ProductPaymentApplication(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, null=True)
    tour = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=50)
    payment_check = models.FileField(upload_to='media/payment_check')
    status = models.CharField(
        max_length=25,
        choices=PaymentApplicationStatusEnum.choices,
        default=PaymentApplicationStatusEnum.IN_PROGRESS
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка на оплату за Тур'
        verbose_name_plural = 'Заявка на оплату за Тур'

