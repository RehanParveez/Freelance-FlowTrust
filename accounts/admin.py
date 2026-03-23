from django.contrib import admin
from accounts.models import User, Profile, VerificationStatus

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
  list_display = ['email', 'phone', 'dob', 'is_active', 'is_staff', 'control', 'date_joined', 'created_at', 'updated_at']
    
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['user', 'bio', 'pic', 'location']
  
@admin.register(VerificationStatus)
class VerificationStatusAdmin(admin.ModelAdmin):
  list_display = ['user', 'is_verified', 'verified_at']