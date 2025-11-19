from django.apps import AppConfig


class GoodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goods'
    verbose_name = 'ТОВАРЫ'

    def ready(self):
        # Импортируем сигналы при запуске приложения
        import goods.signals