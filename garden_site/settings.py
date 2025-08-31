import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные из nano.env
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')

# Режим дебага для продакшн
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Разрешённые хосты
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'uphevo-garden-site-e87c.twc1.net').split(',')

# Почтовый сервер
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.mail.ru')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 465))
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'skazochniysad@mail.ru')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 't3BS4Hmr9jnjVp4yS5dg')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'flowers',
    'ckeditor',
    'ckeditor_uploader',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'garden_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'main', 'templates')],
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

WSGI_APPLICATION = 'garden_site.wsgi.application'

# База данных (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Медиа
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Статика
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# CKEditor
CKEDITOR_UPLOAD_PATH = "uploads/"

# Локализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Novosibirsk'
USE_I18N = True
USE_TZ = True

# Безопасность для дебага
SECURE_SSL_REDIRECT = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Настройки по умолчанию для auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
