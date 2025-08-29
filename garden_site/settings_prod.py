from .settings import *
import os

# -----------------------
# Основные настройки
# -----------------------
DEBUG = False

# Разрешённые хосты для продакшн
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# -----------------------
# Статика и медиа
# -----------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# MEDIA_ROOT указывает на project_root/media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# -----------------------
# Email
# -----------------------
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.mail.ru")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# -----------------------
# Другие настройки продакшн
# -----------------------
# Например, можно добавить безопасные cookies, HTTPS и т.д.
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
