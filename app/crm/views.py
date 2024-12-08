from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from crm.models import TourPayment
from payment_system.choices import PaymentApplicationStatusEnum
from payment_system.models import ProductPaymentApplication

from goods.models import Categories, Products


def payment_request_view(request):

    if not request.user.is_authenticated or not request.user.is_admin and not request.user.status == 2:
        return redirect('main:main_index')

    applications = ProductPaymentApplication.objects.filter(status__in=['in_progress', 'denied']).order_by('-id')

    payment_choices = PaymentApplicationStatusEnum

    return render(
        request=request,
        template_name='crm/payment_request.html',
        context={
            'applications': applications,
            'payment_choices': payment_choices
        }
    )


def payment_request_update_status_view(request, application_id):
    application = get_object_or_404(ProductPaymentApplication, id=application_id)

    if request.method == 'POST':
        if 'status' in request.POST:
            status = request.POST['status']

            if status == 'accepted':
                payment = TourPayment(
                    user=application.user.full_name,
                    tour=application.tour.name,
                    payment_method=application.payment_method,
                    payment_check=application.payment_check
                )
                payment.save()

            application.status = status
            application.save()
            messages.success(request, 'Cтатус изменен!')
            return redirect('payment_applications')

    return redirect('payment_applications')


def dashboard_view(request):
    if not request.user.is_authenticated or not request.user.is_admin and not request.user.status == 2:
        return redirect('main:main_index')

    return render(request, 'crm/dashboard.html')


def tour_payments_view(request):

    return render(request, 'crm/tour_payments.html')

def event_list_view(request, tours=None):
    crm_table = TourFilter(request.GET, queryset=Products.objects.filter(status__in=(2, 3)))

    categories = Categories.objects.all()

    paginator = Paginator(crm_table.qs, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request=request,
        template_name='main/event_list.html',
        context={
            'tours': tours,
            'page_obj': page_obj,
            'categories': categories
        }
    )