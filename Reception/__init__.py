from django.apps import AppConfig
from django.db.models import signals


def start_cron_jobs(sender, **kwargs):
    # Importa el módulo django_cron aquí para evitar problemas de importación circular
    from django_cron import CronJobManager

    # Ejecuta todos los cron jobs registrados
    CronJobManager.run()


class ReceptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Reception'

    def ready(self):
        # Importa tu clase de cron job aquí para que Django la reconozca
        from .cron import MarcarHabitacionesSuciasCronJob

        # Registra tu cron job para ejecutarse cuando se inicie el servidor
        signals.post_migrate.connect(start_cron_jobs, sender=self)
