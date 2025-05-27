from django.apps import AppConfig

class TourismConfig(AppConfig):
    name = 'tourism'

    def ready(self):
        import tourism.signals  # noqa
