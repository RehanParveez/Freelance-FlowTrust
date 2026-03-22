from django.urls import path, include
from accounts.views import UserViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'user', UserViewset, basename = 'user')

urlpatterns = [
  path('', include(router.urls)),
]
