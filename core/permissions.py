from rest_framework.permissions import BasePermission

class ClientPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    if request.user.control == 'client':
      return True
    return False

class FreelancerPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    if request.user.control == 'freelancer':
      return True
    return False

class AdminPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    if request.user.control == 'admin':
      return True
    return False

class OwnerPermission(BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj.user == request.user

class ContractPermission(BasePermission):
  def has_object_permission(self, request, view, obj):
    user = request.user
    if user.control == 'admin':
      return True
    if user == obj.client:
      return True
    if user == obj.freelancer:
      return True
    return False

class MilestonePermission(BasePermission):
  def has_object_permission(self, request, view, obj):
    user = request.user
    contract = obj.contract
    if user.control == 'admin':
      return True
    if user == contract.client:
      return True
    if user == contract.freelancer:
      return True
    return False
        
class PaymentPermission(BasePermission):
  def has_object_permission(self, request, view, obj):
    user = request.user
    if user.control == 'admin':
      return True
    if user == obj.client:
      return True
    if user == obj.freelancer:
      return True
    return False
        
class JobPermission(BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj.client == request.user

class ProposalPermission(BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj.freelancer.user == request.user