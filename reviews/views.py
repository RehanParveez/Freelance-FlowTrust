from rest_framework import viewsets
from reviews.serializers.detail import ReviewSerializer, RatingSerializer
from reviews.models import Review, Rating
from core.permissions import OwnerOrAdminPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from contracts.models import Contract

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
  
  def create(self, request, *args, **kwargs):
    user = request.user
    contr_id = request.data.get('contract')
    if not contr_id:
      return Response({'err': 'the contr is required'}, status=400)
    contr = Contract.objects.filter(id=contr_id)
    contr = contr.first()
    if not contr:
      return Response({'err': 'this is a wrong contr'}, status=400)

    if contr.status != 'completed':
      return Response({'err': 'the contr is not completed'}, status=400)
    if user != contr.client:
      if user != contr.freelancer:
        return Response({'err': 'its not allowed'}, status=403)

    if Review.objects.filter(reviewer=user, contract=contr).exists():
      return Response({'err': 'it is already reviewed'}, status=400)
    if user == contr.client:
      reviewee = contr.freelancer
    else:
      reviewee = contr.client

    Review.objects.create(reviewer=user, reviewee=reviewee, contract=contr, comments=request.data.get('comments'))
    return Response({'msg': 'the review is created'}, status=201)

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
    
    



