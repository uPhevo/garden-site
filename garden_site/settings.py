# garden_site/settings.py
import os
import re
from pathlib import Path
from dotenv import load_dotenv

# load .env (nano.env)
_here = Path(__file__).resolve().parent.parent
load_dotenv(_here / "nano.env")

BASE_DIR = _here

# секрет
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

# DEBUG parsing
_DEBUG_RAW = os.getenv("DEBUG", "False")
DEBUG = str(_DEBUG_RAW).strip().lower() in ("1", "true", "yes", "on")

# ALLOWED_HOSTS parsing (CSV, пробелы, скобки)
_raw_hosts = os.getenv("ALLOWED_HOSTS", "")
if _raw_hosts:
    # убрать скобки и кавычки и разделить
    clean = re.sub(r"^[\[\(]+|[\]\)]+$", "", _raw_hosts).strip()
    ALLOWED_HOSTS = [h.strip() for h in re.split(r"[,\s]+", clean) if h.strip()]
else:
    ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# для удобства при локальном тесте можно добавить 0.0.0.0
if DEBUG and "0.0.0.0" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS += ["0.0.0.0"]

# CSRF trusted origins (если используешь HTTPS через прокси)
CSRF_TRUSTED_ORIGINS = []
for host in ALLOWED_HOSTS:
    if host and host != "*" and host not in ("127.0.0.1", "localhost", "0.0.0.0"):
        host_only = host.split(":")[0]
        CSRF_TRUSTED_ORIGINS.append(f"https://{host_only}")
        # если нужен http версия, можно раскомментировать
        # CSRF_TRUSTED_ORIGINS.append(f"http://{host_only}")

# если сайт за reverse-proxy с X-Forwarded-Proto:
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.mail.ru")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USE_SSL = str(os.getenv("EMAIL_USE_SSL", "True")).strip().lower() in ("1", "true", "yes")
EMAIL_USE_TLS = str(os.getenv("EMAIL_USE_TLS", "False")).strip().lower() in ("1", "true", "yes")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "skazochniysad@mail.ru")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "t3BS4Hmr9jnjVp4yS5dg")
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
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


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

# DATABASE: если есть DATABASE_URL — используем dj_database_url, иначе sqlite
db_url = os.getenv("DATABASE_URL", "")
if db_url:
    try:
        import dj_database_url
        DATABASES = {"default": dj_database_url.parse(db_url, conn_max_age=600, ssl_require=not DEBUG)}
    except Exception:
        # fallback sqlite (если dj_database_url не установлен)
        DATABASES = {
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
        }
else:
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

# media & static
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # обязательно для collectstatic

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

# простой logging — ошибок в файл
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {"class": "logging.FileHandler", "filename": BASE_DIR / "django_errors.log", "encoding": "utf-8"},
    },
    "loggers": {"django": {"handlers": ["file"], "level": "ERROR", "propagate": True}},
}
