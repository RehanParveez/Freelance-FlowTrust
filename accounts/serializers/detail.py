from rest_framework import serializers
from accounts.serializers.basic import ProfileSerializer1, VerificationStatusSerializer1
from accounts.models import User, Profile, VerificationStatus
from marketplace.serializers.basic import FreelancerProfileSerializer1
from payments.serializers.detail import WalletSerializer, PaymentMethodSerializer

class UserSerializer(serializers.ModelSerializer):
  profile = ProfileSerializer1(many=True, read_only=True)
  ver_status = VerificationStatusSerializer1(read_only=True)
  freelancer_prof = FreelancerProfileSerializer1(read_only=True)
  wallet = WalletSerializer(read_only=True)
  pay_methods = PaymentMethodSerializer(many=True, read_only=True)
  class Meta:
    model = User
    fields = ['email', 'username', 'profile', 'ver_status', 'freelancer_prof', 'wallet', 'pay_methods', 'phone', 'dob', 'is_active', 'is_staff', 'control', 'date_joined', 'created_at', 'updated_at']
  
  def create(self, validated_data):
    user=User.objects.create_user(
    username=validated_data.get('username'),
    email=validated_data.get('email'),
    password=validated_data.get('password'),
    phone=validated_data.get('phone'),
    dob=validated_data.get('dob'),
    is_active=validated_data.get('is_active'),
    is_staff=validated_data.get('is_staff'),
    date_joined=validated_data.get('date_joined'),
    created_at=validated_data.get('created_at'),
    updated_at=validated_data.get('updated_at'),  
    )
    return user

class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = Profile
    fields = ['user', 'bio', 'pic', 'location']
    
class VerificationStatusSerializer(serializers.ModelSerializer):
  class Meta:
    model = VerificationStatus
    fields = ['user', 'is_verified', 'verified_at']