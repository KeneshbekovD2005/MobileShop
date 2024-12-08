from django.db import models


class PaymentApplicationStatusEnum(models.TextChoices):
    IN_PROGRESS = 'in_progress', 'В обработке'
    DENIED = 'denied', 'Отклонено'
    ACCEPTED = 'accepted', 'Принято'