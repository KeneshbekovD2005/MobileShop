from django.urls import path
from . import views

app_name = 'goods'

urlpatterns = [
    path('search/', views.categories_view, name='search'),
    path('user-like/<int:user_id>/<slug:product_slug>/', views.user_like_tour_view, name='tour_like'),  # Перемещен выше
    path('product/<int:product_id>/', views.product_view, name='product'),
    path('product/<slug:product_slug>/', views.product_view, name='product'),
    path('<slug:category_slug>/', views.categories_view, name='categories_index'),
    path('user-likes/', views.user_likes, name='user_likes')
]
