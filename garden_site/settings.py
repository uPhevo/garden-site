import os
import re
from pathlib import Path
from dotenv import load_dotenv
from whitenoise import WhiteNoise

# load .env (nano.env)
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "nano.env")

# Секретный ключ
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

# DEBUG parsing
_DEBUG_RAW = os.getenv("DEBUG", "True")
DEBUG = str(_DEBUG_RAW).strip().lower() in ("1", "true", "yes", "on")

# ALLOWED_HOSTS parsing (CSV, пробелы, скобки)
_raw_hosts = os.getenv("ALLOWED_HOSTS", "")
if _raw_hosts:
    clean = re.sub(r"^[\[\(]+|[\]\)]+$", "", _raw_hosts).strip()
    ALLOWED_HOSTS = [h.strip() for h in re.split(r"[,\s]+", clean) if h.strip()]
else:
    ALLOWED_HOSTS = []

# Добавляем явно домен Timeweb и IP сервера
ALLOWED_HOSTS += [
    "uphevo-garden-site-e87c.twc1.net",
    "www.uphevo-garden-site-e87c.twc1.net",
    "188.225.37.139",
]

# Для локального теста можно оставить 127.0.0.1 и localhost
if DEBUG:
    ALLOWED_HOSTS += ["127.0.0.1", "localhost", "0.0.0.0"]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host not in ("127.0.0.1", "localhost", "0.0.0.0")]

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.mail.ru")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USE_SSL = str(os.getenv("EMAIL_USE_SSL", "True")).strip().lower() in ("1", "true", "yes")
EMAIL_USE_TLS = str(os.getenv("EMAIL_USE_TLS", "False")).strip().lower() in ("1", "true", "yes")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)

# apps / middleware
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main",
    "flowers",
    "ckeditor",
    "ckeditor_uploader",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # WhiteNoise для статики
]

ROOT_URLCONF = "garden_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "main" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "garden_site.wsgi.application"

# DATABASE
db_url = os.getenv("DATABASE_URL", "")
if db_url:
    try:
        import dj_database_url
        DATABASES = {"default": dj_database_url.parse(db_url, conn_max_age=600, ssl_require=not DEBUG)}
    except Exception:
        DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

# media & static
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # обязательно для collectstatic
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"  # WhiteNoise storage

# CKEditor
CKEDITOR_UPLOAD_PATH = "uploads/"

# локализация
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Asia/Novosibirsk"
USE_I18N = True
USE_TZ = True

# безопасность (в debug отключаем редиректы)
SECURE_SSL_REDIRECT = False if DEBUG else True
CSRF_COOKIE_SECURE = False if DEBUG else True
SESSION_COOKIE_SECURE = False if DEBUG else True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
