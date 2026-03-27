from rest_framework.permissions import BasePermission

class AdminPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    if request.user.control == 'admin':
      return True
    
    return False
  
  def has_object_permission(self, request, view, obj):
    return request.user.control == 'admin'
  
class ClientPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    if request.user.control == 'client':
      return True
    
    return False

  def has_object_permission(self, request, view, obj):
    if type(obj).__name__ == 'Contract':
      return obj.client == request.user
    if type(obj).__name__ == 'Proposal':
        return obj.job.client == request.user
    if type(obj).__name__ in ['Wallet', 'Profile']:
      return obj.user == request.user
    
    return False
  
class FreelancerPermission(BasePermission):
  def has_permission(self, request, view):
    if not request.user.is_authenticated:
      return False
    if request.user.control == 'freelancer':
      return True
    
    return False

  def has_object_permission(self, request, view, obj):
    user = request.user
    obj_type = type(obj).__name__
    if obj_type == 'Contract':
      return obj.freelancer == user
    if obj_type == 'Proposal':
      return obj.freelancer.user == user
    if obj_type == 'Milestone':
      return obj.contract.freelancer == user
    if obj_type == 'Message':
      return obj.by == user

    return False

class OwnerOrAdminPermission(BasePermission):
  def has_permission(self, request, view):
    return request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    user = request.user
    if user.control == 'admin':
      return True
    if hasattr(obj, 'client') and hasattr(obj, 'freelancer'):
      if obj.client == user or obj.freelancer == user:
        return True

    contract_related_models = [
        'ContrParticipant', 'ContractTerm', 'ContractStatus', 'Activity', 'Milestone', 'MilestoneSubmission', 'MilestoneReview', 'MilestoneStatus',
            'Dispute', 'DisputeMessage', 'Proof', 'Payment', 'Escrow', 'Wallet', 'Transaction', 'Refund', 'PaymentMethod']
    if obj.__class__.__name__ in contract_related_models:
      if hasattr(obj, 'contract') and (obj.contract.client == user or obj.contract.freelancer == user):
        return True
      if hasattr(obj, 'escrow') and (obj.escrow.client == user or obj.escrow.freelancer == user):
          return True
      if hasattr(obj, 'wallet') and obj.wallet.user == user:
          return True
      if hasattr(obj, 'payment') and (obj.payment.client == user or obj.payment.freelancer == user):
        return True
      if hasattr(obj, 'milestone') and hasattr(obj.milestone, 'contract'):
        if obj.milestone.contract.client == user or obj.milestone.contract.freelancer == user:
          return True
  
    user_related_models = [
      'Profile', 'VerificationStatus', 'Skill', 'FreelancerProfile', 'Portfolio', 'JobPost', 'Proposal', 'Review', 'Rating', 'Notification', 'UserAnalytics', 'EarningReport', 'ContractAnalytics']
    if obj.__class__.__name__ in user_related_models:
      if hasattr(obj, 'user') and obj.user == user:
        return True
      if hasattr(obj, 'freelancer') and hasattr(obj.freelancer, 'user') and obj.freelancer.user == user:
        return True
      if hasattr(obj, 'reviewer') and obj.reviewer == user:
        return True
      if hasattr(obj, 'reviewee') and obj.reviewee == user:
        return True

    return False
  
