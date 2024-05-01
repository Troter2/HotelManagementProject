from django.apps import AppConfig


class ReceptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Reception'
    def ready(self):
        import Reception.signals
