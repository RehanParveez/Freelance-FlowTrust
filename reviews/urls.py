from django.urls import path, include
from reviews.views import ReviewViewset, RatingViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'review', ReviewViewset, basename = 'review')
router.register(r'rating', RatingViewset, basename = 'rating')

urlpatterns = [
  path('', include(router.urls)),
]