from itertools import product
from lib2to3.fixes.fix_input import context
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg, DecimalField
from django.shortcuts import render, get_object_or_404, redirect
from pyexpat.errors import messages
from unicodedata import category
from django.contrib import messages
from goods.models import Products, Categories, Rating, Favorite
from goods.utils import q_search
from payment_system.models import PaymentMethod
from user.models import MyUser


def categories_view(request, category_slug=None):

    categories = Categories.objects.all()
    page = request.GET.get('page', 1)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Products.objects.filter(category__slug=category_slug)


    paginator = Paginator(goods, 6)
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)

    context = {
        "categories": categories,
        "goods": current_page,
    }
    return render(request, 'goods/categories.html', context=context)


def product_view(request, product_id=None, product_slug=None):
    if product_id:
        product = get_object_or_404(Products, id=product_id)
    elif product_slug:
        product = get_object_or_404(Products, slug=product_slug)
    else:
        return redirect('categories_view')

    similar_products = Products.objects.filter(category=product.category).exclude(slug=product.slug)
    product_ratings = Rating.objects.filter(product=product).aggregate(Avg("recall"))['recall__avg']
    payment_methods = PaymentMethod.objects.filter(is_active=True)

    if product_ratings is not None:
        product_ratings = round(product_ratings, 2)

    if request.method == "POST" and "rating" in request.POST:
        rating = int(request.POST["rating"])
        product_rating = Rating(user=request.user, product=product, recall=rating)
        product_rating.save()
        messages.success(request, "Спасибо за отзыв")
        return redirect('goods:product', product_slug=product.slug)

    context = {
        "product": product,
        "similar_products": similar_products,
        "product_ratings": product_ratings,
        "payment_methods": payment_methods,
    }
    return render(request, 'goods/product.html', context=context)



from django.shortcuts import get_object_or_404, redirect
from .models import MyUser, Products, Favorite

def user_like_tour_view(request, user_id, product_slug):
    user = get_object_or_404(MyUser, id=user_id)
    product = get_object_or_404(Products, slug=product_slug)
    favorite = Favorite.objects.filter(user=user, tour=product).first()

    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(user=user, tour=product)
        messages.success(request, "Посмотрите свои лайки")


    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def user_likes(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('tour')
    print(favorites)

    return render(request, 'goods/user_likes.html', {'favorites': favorites})
