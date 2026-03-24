from rest_framework import serializers
from accounts.models import User, Profile, VerificationStatus

class UserSerializer1(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['email', 'username', 'phone', 'is_active', 'created_at']

class ProfileSerializer1(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['user', 'bio']
    
class VerificationStatusSerializer1(serializers.ModelSerializer):
  class Meta:
    model = VerificationStatus
    fields = ['user', 'is_verified']