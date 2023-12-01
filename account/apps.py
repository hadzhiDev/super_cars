from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    verbose_name = 'Аккаунты'

    # def ready(self):
    #     import account.signals  # Add this line to import the signals.py
