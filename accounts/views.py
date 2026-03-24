from django.shortcuts import render
from rest_framework import viewsets
from accounts.serializers.detail import UserSerializer
from accounts.models import User

# Create your views here.
class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')
  
