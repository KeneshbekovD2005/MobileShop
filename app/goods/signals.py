from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Comment


@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    """
    Отправляет email пользователю при создании нового комментария
    """
    if created:
        try:
            # Получаем email пользователя, который оставил комментарий
            user_email = instance.user.email
            product_name = instance.product.name

            # Используем full_name из модели MyUser
            if instance.user.full_name and instance.user.full_name.strip():
                user_name = instance.user.full_name.strip()
            elif instance.user.first_name:
                user_name = instance.user.first_name
            else:
                user_name = user_email  # Если нет имени, используем email

            subject = f'Новый комментарий к товару "{product_name}"'
            message = f'''
Здравствуйте, {user_name}!

Вы оставили комментарий к товару "{product_name}".

Текст вашего комментария:
"{instance.text}"

Дата: {instance.created_date.strftime("%d.%m.%Y %H:%M")}

Спасибо за ваш отзыв!

---
С уважением,
Команда магазина MobileShop 
Директор магазина Daniel Keneshbekov
'''

            # Отправляем email пользователю
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user_email],
                fail_silently=False,
            )
            print(f"✅ Email отправлен на {user_email}")

        except Exception as e:
            print(f"❌ Ошибка при отправке email: {e}")