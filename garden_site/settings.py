import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Загружаем переменные из nano.env
load_dotenv('nano.env')

BASE_DIR = Path(__file__).resolve().parent.parent

# -----------------------
# Основные настройки
# -----------------------
SECRET_KEY = os.getenv("SECRET_KEY", "your-very-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"

# ALLOWED_HOSTS (разделяем CSV из .env)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS]

# -----------------------
# Почта
# -----------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.mail.ru")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "skazochniysad@mail.ru")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# -----------------------
# Приложения
# -----------------------
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

# Разрешенные домены для CSRF-запросов
CSRF_TRUSTED_ORIGINS = [
    'https://uphevo-garden-site-e87c.twc1.net',
    'https://www.uphevo-garden-site-e87c.twc1.net',  # если нужен www
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
        'DIRS': [BASE_DIR / 'main' / 'templates'],
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

# -----------------------
# База данных
# -----------------------
db_url = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
DATABASES = {
    "default": dj_database_url.parse(db_url, conn_max_age=600, ssl_require=not DEBUG)
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------
# Статика и медиа
# -----------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # collectstatic соберёт сюда

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------
# CKEditor
# -----------------------
CKEDITOR_UPLOAD_PATH = "uploads/"

# -----------------------
# Локализация
# -----------------------
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Novosibirsk'
USE_I18N = True
USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
    },
}
