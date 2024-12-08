from django.db import models


class TourPayment(models.Model):
    user = models.CharField(max_length=225)
    tour = models.CharField(max_length=350)
    payment_method = models.CharField(max_length=50)
    payment_check = models.FileField(upload_to='media/payment_check')
    created_date = models.DateTimeField(auto_now_add=True)


