from django.shortcuts import render
from rest_framework import viewsets
from reviews.serializers.detail import ReviewSerializer, RatingSerializer
from reviews.models import Review, Rating
from core.permissions import ReviewPermission

# Create your views here.
class ReviewViewset(viewsets.ModelViewSet):
  serializer_class = ReviewSerializer
  queryset = Review.objects.all().order_by('id')
  permission_classes = [ReviewPermission]

class RatingViewset(viewsets.ModelViewSet):
  serializer_class = RatingSerializer
  queryset = Rating.objects.all().order_by('id')
  permission_classes = [ReviewPermission]
    
    



