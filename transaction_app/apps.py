from django.apps import AppConfig


class TransactionAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transaction_app'

    def ready(self):
        import transaction_app.signals
