from django.urls import path, include
from contracts.views import ContractViewset, ContrParticipantViewset, ContractTermViewset, ContractStatusViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'contract', ContractViewset, basename = 'contract')
router.register(r'contractparticipant', ContrParticipantViewset, basename = 'contractparticipant')
router.register(r'contractterm', ContractTermViewset, basename = 'contractterm')
router.register(r'contractstatus', ContractStatusViewset, basename = 'contractstatus')

urlpatterns = [
  path('', include(router.urls)),
]