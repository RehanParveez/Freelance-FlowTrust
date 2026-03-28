from django.apps import AppConfig

class DisputesConfig(AppConfig):
    name = 'disputes'
    
    def ready(self):
      import disputes.signals
