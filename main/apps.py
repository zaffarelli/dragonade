from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        pass
        import main.signals.autochtons
        import main.signals.travellers
        import main.signals.dreams
        import main.signals.equipement
