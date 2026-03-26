from django.urls import path, include
from disputes.views import DisputeViewset, DisputeMessageViewset, ProofViewset, SolutionViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'dispute', DisputeViewset, basename = 'dispute')
router.register(r'disputemessage', DisputeMessageViewset, basename = 'disputemessage')
router.register(r'proof', ProofViewset, basename = 'proof')
router.register(r'solution', SolutionViewset, basename = 'solution')

urlpatterns = [
  path('', include(router.urls)),
]

