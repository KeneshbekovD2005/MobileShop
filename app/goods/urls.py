from django.urls import path
from . import views

app_name = 'goods'

urlpatterns = [
    path('search/', views.categories_view, name='search'),
    path('user-like/<int:user_id>/<slug:product_slug>/', views.user_like_tour_view, name='tour_like'),
    path('product/<int:product_id>/', views.product_view, name='product'),
    path('product/<slug:product_slug>/', views.product_view, name='product'),
    path('<slug:category_slug>/', views.categories_view, name='categories_index'),
    path('user-likes/', views.user_likes, name='user_likes'),
    path('comment/add/<slug:product_slug>/', views.add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('remove-like/<int:favorite_id>/', views.remove_like, name='remove_like'),
]