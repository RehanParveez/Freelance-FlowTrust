from django.urls import path, include
from payments.views import PaymentViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'payment', PaymentViewset, basename = 'payment')

urlpatterns = [
  path('', include(router.urls)),
]
