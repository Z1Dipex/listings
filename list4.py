# Используем get_or_create чтобы не было ошибки при первом входе
user_report, created = DatasetOtchet.objects.get_or_create(user=request.user)  # Разные user_id

# Настройка сессий (settings.py)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600 
SESSION_SAVE_EVERY_REQUEST = True 
