from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        import main.signals.nativi
        import main.signals.viaggiatori
        import main.signals.creature
        import main.signals.contestants
        import main.signals.combats
        import main.signals.sogni
        import main.signals.equipement
        import main.signals.incantessimi
        import main.signals.artefatti
