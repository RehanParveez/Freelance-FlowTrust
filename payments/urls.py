from django.urls import path, include
from payments.views import WalletViewset, PaymentViewset, PaymentMethodViewset
from rest_framework.routers import DefaultRouter 

router = DefaultRouter()
router.register(r'wallet', WalletViewset, basename = 'wallet')
router.register(r'payment', PaymentViewset, basename = 'payment')
router.register(r'paymentmethod', PaymentMethodViewset, basename = 'paymentmethod')

urlpatterns = [
  path('', include(router.urls)),
]
