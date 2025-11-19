from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from user.models import MyUser


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='media/categories_images', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ("id",)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    descriptions = models.TextField(max_length=1000, blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='media/product_images', blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, verbose_name='Цена')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Нету в наличии'),
            (2, 'В продаже'),
        ),
        default=1,
        verbose_name='Статус'
    )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='user_likes')
    tour = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_likes')
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Rating(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    recall = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, verbose_name='Текст комментария')  # Ограничение до 500 символов
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created_date',)

    def __str__(self):
        return f'Комментарий от {self.user} к {self.product}'

    def get_display_name(self):
        """Получает отображаемое имя пользователя"""
        if hasattr(self.user, 'get_full_name') and self.user.get_full_name():
            return self.user.get_full_name()
        elif hasattr(self.user, 'first_name') and self.user.first_name:
            return self.user.first_name
        else:
            return self.user.username