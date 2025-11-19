from itertools import product
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from goods.models import Products, Categories, Rating, Favorite, Comment
from goods.forms import CommentForm
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
    rating_count = Rating.objects.filter(product=product).count()
    payment_methods = PaymentMethod.objects.filter(is_active=True)

    # Получаем комментарии с информацией о пользователях и сортируем по дате
    comments = Comment.objects.filter(product=product, is_active=True).select_related('user').order_by('-created_date')

    # Добавляем отображаемые имена для комментариев
    for comment in comments:
        comment.display_name = comment.get_display_name()

    # Проверка лайка пользователя
    user_like_check = False
    user_rating = None
    if request.user.is_authenticated:
        user_like_check = Favorite.objects.filter(user=request.user, tour=product).exists()
        # Получаем оценку текущего пользователя
        user_rating_obj = Rating.objects.filter(user=request.user, product=product).first()
        if user_rating_obj:
            user_rating = user_rating_obj.recall

    if product_ratings is not None:
        product_ratings = round(product_ratings, 2)

    # Обработка рейтинга
    if request.method == "POST" and "rating" in request.POST:
        if not request.user.is_authenticated:
            messages.error(request, "Для оценки необходимо авторизоваться")
            return redirect('goods:product', product_slug=product.slug)

        rating = int(request.POST["rating"])
        existing_rating = Rating.objects.filter(user=request.user, product=product).first()
        if existing_rating:
            existing_rating.recall = rating
            existing_rating.save()
            messages.success(request, "Ваша оценка обновлена")
        else:
            product_rating = Rating(user=request.user, product=product, recall=rating)
            product_rating.save()
            messages.success(request, "Спасибо за оценку")
        return redirect('goods:product', product_slug=product.slug)

    # Обработка комментариев
    comment_form = CommentForm()
    if request.method == "POST" and "text" in request.POST:
        if not request.user.is_authenticated:
            messages.error(request, "Для комментирования необходимо авторизоваться")
            return redirect('goods:product', product_slug=product.slug)

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            messages.success(request, "Комментарий добавлен")
            return redirect('goods:product', product_slug=product.slug)
        else:
            # Показываем ошибки валидации
            for error in comment_form.errors.values():
                messages.error(request, error)

    context = {
        "product": product,
        "similar_products": similar_products,
        "product_ratings": product_ratings,
        "rating_count": rating_count,
        "payment_methods": payment_methods,
        "comments": comments,
        "comment_form": comment_form,
        "user_like_check": user_like_check,
        "user_rating": user_rating,
    }
    return render(request, 'goods/product.html', context=context)


@login_required
def add_comment(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.user = request.user
            comment.save()
            messages.success(request, "Комментарий добавлен")
        else:
            # Показываем ошибки валидации
            for error in form.errors.values():
                messages.error(request, error)

    return redirect('goods:product', product_slug=product_slug)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Проверяем, что пользователь является автором комментария
    if comment.user == request.user or request.user.is_staff:
        comment.delete()
        messages.success(request, "Комментарий удален")
    else:
        messages.error(request, "Вы не можете удалить этот комментарий")

    return redirect('goods:product', product_slug=comment.product.slug)


def user_like_tour_view(request, user_id, product_slug):
    # Проверяем, что пользователь авторизован и это его ID
    if not request.user.is_authenticated or request.user.id != user_id:
        messages.error(request, "У вас нет прав для этого действия")
        return redirect('goods:product', product_slug=product_slug)

    user = get_object_or_404(MyUser, id=user_id)
    product = get_object_or_404(Products, slug=product_slug)
    favorite = Favorite.objects.filter(user=user, tour=product).first()

    if favorite:
        favorite.delete()
        messages.success(request, "Удалено из избранного")
    else:
        Favorite.objects.create(user=user, tour=product)
        messages.success(request, "Добавлено в избранное")

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_like(request, favorite_id):
    """Удаление лайка со страницы 'Мои лайки'"""
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    favorite.delete()
    messages.success(request, "Лайк удален")
    return redirect('goods:user_likes')


@login_required
def user_likes(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('tour')
    return render(request, 'goods/user_likes.html', {'favorites': favorites})