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
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    user = request.user
    if user.control == 'admin':
      return True
    return user in [obj.client, obj.freelancer]

class MilestonePermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    user = request.user
    contract = obj.contract
    if user.control == 'admin':
      return True
    return user in [contract.client, contract.freelancer]
        
class PaymentPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    user = request.user
    if user.control == 'admin':
      return True
    return user in [obj.client, obj.freelancer]
        
class JobPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    return obj.client == request.user

class ProposalPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    return obj.freelancer.user == request.user
  
class DisputePermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    user = request.user
    if user.control == 'admin':
      return True
    return user in [obj.contract.client, obj.contract.freelancer]

class DisputeMessagePermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    user = request.user
    if user.control == 'admin':
      return True
    return user in [obj.dispute.contract.client, obj.dispute.contract.freelancer]
  
class ProofPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    user = request.user
    if user.control == 'admin':
      return True
    return user in [obj.dispute.contract.client, obj.dispute.contract.freelancer]
  
class SolutionPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated and request.user.control == 'admin'
  
class TalkPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    return request.user in obj.participants.all()
  
class MessagePermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    return obj.by == request.user
  
class NegotiationPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    user = request.user
    if user.control == 'admin':
      return True
    return user in [obj.contract.client, obj.contract.freelancer]
  
class ReviewPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    return obj.reviewer == request.user
  
class AnalyticsPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated
  
class NotificationPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    return obj.user == request.user

class ActivityPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    user = request.user
    if user.control == 'admin':
      return True
    return obj.user == user