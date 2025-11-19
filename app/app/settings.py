"""
Django settings for app project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-p4!vak1*d)r^i^*i%rr=4yrv1bec1v3cgl(o4t2oqf(@p3utr)'

# Определяем, работает ли на PythonAnywhere
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com', 'localhost', '127.0.0.1']

# Если нужно временно включить DEBUG для отладки:
# DEBUG = os.environ.get('DEBUG', 'False') == 'True'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # your apps
    'main',
    'goods.apps.GoodsConfig',  # Изменено для работы с сигналами
    'user',
    'payment_system',
    'crm',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Добавьте Whitenoise для статических файлов
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    # НУЖНЫЙ middleware для смены языка
    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTH_USER_MODEL = 'user.MyUser'

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------
#       I18N / TRANSLATION
# -------------------------------

LANGUAGE_CODE = 'ru'        # язык по умолчанию
TIME_ZONE = 'UTC'

USE_I18N = True
USE_TZ = True

# Доступные языки
LANGUAGES = [
    ('ru', 'Russian'),
    ('en', 'English'),
]

# Папка, где будут храниться файлы перевода
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# -------------------------------
#       EMAIL CONFIGURATION
# -------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'danielkeneshbekov1997@gmail.com'
EMAIL_HOST_PASSWORD = 'zawa jysa hgsz bloo'
DEFAULT_FROM_EMAIL = 'danielkeneshbekov1997@gmail.com'

# -------------------------------
#       STATIC FILES (ОБНОВЛЕНО ДЛЯ DEPLOY)
# -------------------------------

STATIC_URL = '/static/'

# Для разработки
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Для продакшена - куда collectstatic соберет файлы
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Настройки Whitenoise для сжатия статических файлов
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------
#       SECURITY SETTINGS (ДОБАВЛЕНО)
# -------------------------------

# Безопасность cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# HSTS settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Другие security настройки
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'