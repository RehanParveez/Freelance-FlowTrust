from django.apps import AppConfig

class MilestonesConfig(AppConfig):
    name = 'milestones'
    
    def ready(self):
      import milestones.signals
