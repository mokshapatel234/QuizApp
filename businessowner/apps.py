from django.apps import AppConfig


class BusinessownerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'businessowner'

    def ready(self):
        import businessowner.signals


