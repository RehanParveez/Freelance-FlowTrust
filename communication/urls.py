from django.urls import path, include
from communication.views import TalkViewset, MessageViewset, NegotiationViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'talk', TalkViewset, basename = 'talk')
router.register(r'message', MessageViewset, basename = 'message')
router.register(r'negotiation', NegotiationViewset, basename = 'negotiation')

urlpatterns = [
  path('', include(router.urls)),
]