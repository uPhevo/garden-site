#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    # Если переменная окружения DJANGO_SETTINGS_MODULE не задана, используем продакшн-настройки
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'garden_site.settings_prod'
    )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедись, что оно установлено и активна виртуальная среда."
        ) from exc

    execute_from_command_line(sys.argv)
