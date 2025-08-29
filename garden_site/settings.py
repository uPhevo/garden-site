import os
from pathlib import Path

# ----------------------------
# Базовые директории
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------
# Основные настройки
# ----------------------------
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'replace-this-with-a-secure-key')
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'uphevo-garden-site-e87c.twc1.net',
]

# ----------------------------
# Приложения
# ----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'flowers',
    'django_ckeditor_5',
]

# ----------------------------
# Middleware
# ----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project_root.urls'

# ----------------------------
# Шаблоны
# ----------------------------
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

WSGI_APPLICATION = 'project_root.wsgi.application'

# ----------------------------
# База данных (Postgres пример)
# ----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'garden_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# ----------------------------
# Пароли и валидация
# ----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ----------------------------
# Локализация
# ----------------------------
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Novosibirsk'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ----------------------------
# Статика и медиа
# ----------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ----------------------------
# Сессии
# ----------------------------
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ----------------------------
# CSRF и доверенные домены
# ----------------------------
CSRF_TRUSTED_ORIGINS = [
    'https://uphevo-garden-site-e87c.twc1.net',
]

# ----------------------------
# Почта (SMTP)
# ----------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER', 'skazochniysad@mail.ru')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'your-email-password')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ----------------------------
# Безопасность для продакшена
# ----------------------------
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
