from django.urls import path, include
from contracts.views import ContractViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'contract', ContractViewset, basename = 'contract')

urlpatterns = [
  path('', include(router.urls)),
]