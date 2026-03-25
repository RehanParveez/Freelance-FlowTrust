from django.shortcuts import render
from rest_framework import viewsets
from accounts.serializers.detail import UserSerializer, ProfileSerializer, VerificationStatusSerializer
from accounts.models import User, Profile, VerificationStatus
from rest_framework.permissions import IsAuthenticated
from core.permissions import OwnerPermission

# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
      user = self.request.user
      if user.control == 'admin':
        return self.queryset
      return self.queryset.filter(id=user.id)
    
class ProfileViewset(viewsets.ModelViewSet):
  serializer_class = ProfileSerializer
  queryset = Profile.objects.all().order_by('id')
  permission_classes = [OwnerPermission]
  
  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)
  
class VerificationStatusViewset(viewsets.ModelViewSet):
  serializer_class = VerificationStatusSerializer
  queryset = VerificationStatus.objects.all().order_by('id')
  permission_classes = [IsAuthenticated, OwnerPermission]
  
  def get_queryset(self):
    return self.queryset.filter(user=self.request.user)
  
