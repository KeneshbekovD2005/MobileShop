
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls' , namespace= 'main')),
    path('categories/', include('goods.urls' ,namespace='categories')),
    path('product/', include('goods.urls' ,namespace='product')),
    path('user/', include('user.urls' ,namespace='user')),
    path('payment/', include('payment_system.urls', namespace='payment_system')),
    path('crm/', include('crm.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
