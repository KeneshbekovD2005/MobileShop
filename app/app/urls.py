from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns


urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('categories/', include('goods.urls', namespace='categories')),
    path('product/', include('goods.urls', namespace='product')),
    path('user/', include('user.urls', namespace='user')),
    path('payment/', include('payment_system.urls', namespace='payment_system')),
    path('crm/', include('crm.urls')),
    prefix_default_language=True
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path('i18n/', include('django.conf.urls.i18n')),
]