from rest_framework import viewsets
from reviews.serializers.detail import ReviewSerializer, RatingSerializer
from reviews.models import Review, Rating
from core.permissions import OwnerOrAdminPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
class ReviewViewset(viewsets.ModelViewSet):
  serializer_class = ReviewSerializer
  queryset = Review.objects.all().order_by('id')
  permission_classes = [OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['comments']
  ordering_fields = ['created_at']
  filterset_fields = ['comments', 'created_at']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    given = self.queryset.filter(reviewer=user)
    got = self.queryset.filter(reviewee=user)
    return given | got

class RatingViewset(viewsets.ModelViewSet):
  serializer_class = RatingSerializer
  queryset = Rating.objects.all().order_by('id')
  permission_classes = [OwnerOrAdminPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
  # filtering fields
  search_fields = ['score']
  ordering_fields = ['quantity']
  filterset_fields = ['score', 'quantity', 'professionalism']
  
  def get_queryset(self):
    user = self.request.user
    if user.control == 'admin':
      return self.queryset
    given = self.queryset.filter(review__reviewer=user)
    got = self.queryset.filter(review__reviewee=user)
    return given | got
    
    



