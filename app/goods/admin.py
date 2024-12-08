from collections.abc import Sequence
from django.contrib import admin
from goods.models import Categories, Products, Rating , Favorite


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'descriptions')


admin.site.register(Favorite)
admin.site.register(Rating)
