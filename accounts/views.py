from django.shortcuts import render
from rest_framework import viewsets
from accounts.serializers.detail import UserSerializer, ProfileSerializer, VerificationStatusSerializer
from accounts.models import User, Profile, VerificationStatus
from rest_framework.permissions import IsAuthenticated
from core.permissions import OwnerPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # filtering fields
    search_fields = ['email']
    ordering_fields = ['created_at']
    filterset_fields = ['dob', 'is_active', 'is_staff', 'updated_at', 'created_at']
    
    def get_queryset(self):
      user = self.request.user
      if user.control == 'admin':
        return self.queryset
      return self.queryset.filter(id=user.id)
    
class ProfileViewset(viewsets.ModelViewSet):
  serializer_class = ProfileSerializer
  queryset = Profile.objects.all().order_by('id')
  permission_classes = [OwnerPermission]
  filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
  # filtering fields
  search_fields = ['location']
  filterset_fields = ['bio', 'location']
  
  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)
  
class VerificationStatusViewset(viewsets.ModelViewSet):
  serializer_class = VerificationStatusSerializer
  queryset = VerificationStatus.objects.all().order_by('id')
  permission_classes = [IsAuthenticated, OwnerPermission]
  filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    
  # filtering fields
  ordering_fields = ['verified_at']
  filterset_fields = ['is_verified', 'verified_at']
  
  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)
  
