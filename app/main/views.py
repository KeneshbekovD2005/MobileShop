from django.shortcuts import render
from goods.models import Categories , Products
from user.forms import MyUserRegisterForm
from user.models import MyUser


def index(request):
    categories = Categories.objects.all()
    goods = Products.objects.all()
    register_form = MyUserRegisterForm()
    context = {
        "goods": goods,
        "categories": categories,
        "register_form": register_form
    }
    return render(request, 'main/index.html', context=context)


