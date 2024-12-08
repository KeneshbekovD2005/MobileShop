from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


from .models import PaymentMethod, ProductPaymentApplication
from goods.models import Products


def payment_application_order_view(request, payment_method_id, tour_id):
    if not request.user.is_authenticated:
        messages.info(request, 'Пожалуйста зарегистрируйтесь!')
        return redirect('goods:product', product_id=tour_id)

    payment_method = get_object_or_404(PaymentMethod, id=payment_method_id)
    tour = get_object_or_404(Products, id=tour_id)

    if request.method == 'POST':
        if 'check' in request.FILES:
            check = request.FILES['check']

            payment_application_order = ProductPaymentApplication(
                user=request.user,
                tour=tour,
                payment_method=payment_method.title,
                payment_check=check
            )
            payment_application_order.save()
            messages.success(request, 'Заявка отправлена на обработку')
            return redirect('goods:product', product_id=tour.id)  # Перенаправление на страницу продукта

    return render(
        request=request,
        template_name='payment_system/payment_application_order.html',
        context={
            'payment_method': payment_method,
            'tour': tour
        }
    )




def my_payment_application_view(request):
    applications = ProductPaymentApplication.objects.filter(user=request.user)

    return render(
        request=request,
        template_name='payment_system/my_payment_application.html',
        context={
            'applications': applications
        }
    )


