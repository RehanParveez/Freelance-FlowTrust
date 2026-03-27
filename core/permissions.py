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

    if hasattr(obj, 'user') and obj.user == user:
      return True

    if hasattr(obj, 'client') and obj.client == user:
      return True

    if hasattr(obj, 'freelancer'):
      freelancer = obj.freelancer
      if hasattr(freelancer, 'user'):
        if freelancer.user == user:
          return True
      elif freelancer == user:
          return True
    
    if obj.__class__.__name__ == 'ContrParticipant' and hasattr(obj, 'contract'):
      if obj.contract.client == user:
        return True
      
    if obj.__class__.__name__ == 'ContractTerm' and hasattr(obj, 'contract'):
      if obj.contract.client == user:
        return True
    
    if obj.__class__.__name__ == 'ContractStatus' and hasattr(obj, 'contract'):
      if obj.contract.client == user:
        return True
      
    if obj.__class__.__name__ == 'ContractAnalytics' and hasattr(obj, 'contract'):
      if obj.contract.client == user:
        return True

    if hasattr(obj, 'contract') and obj.__class__.__name__ in ['Milestone', 'MilestoneSubmission', 'MilestoneReview', 'MilestoneStatus', 'Escrow', 'Payment', 'Dispute', 'DisputeMessage']:
      contract = obj.contract
      if contract.client == user or contract.freelancer == user:
        return True

    if hasattr(obj, 'milestone'):
      milestone = obj.milestone
      if hasattr(milestone, 'contract'):
        contract = milestone.contract
        if contract.client == user or contract.freelancer == user:
          return True

    if hasattr(obj, 'submission'):
      submission = obj.submission
      if hasattr(submission, 'milestone') and hasattr(submission.milestone, 'contract'):
        contract = submission.milestone.contract
        if contract.client == user or contract.freelancer == user:
          return True
    if hasattr(obj, 'job') and hasattr(obj.job, 'client'):
      if obj.job.client == user:
        return True

    if hasattr(obj, 'freelancer') and hasattr(obj.freelancer, 'user'):
      if obj.freelancer.user == user:
        return True

    if hasattr(obj, 'dispute'):
      dispute = obj.dispute
      if hasattr(dispute, 'contract'):
        contract = dispute.contract
        if contract.client == user or contract.freelancer == user:
          return True

    if hasattr(obj, 'escrow'):
      escrow = obj.escrow
      if escrow.client == user or escrow.freelancer == user:
        return True

    if hasattr(obj, 'payment'):
      payment = obj.payment
      if payment.client == user or payment.freelancer == user:
        return True

    if hasattr(obj, 'wallet') and obj.wallet.user == user:
      return True

    if hasattr(obj, 'reviewer') and obj.reviewer == user:
      return True

    if hasattr(obj, 'reviewee') and obj.reviewee == user:
      return True
    
    if hasattr(obj, 'review'):
      review = obj.review
      if hasattr(review, 'reviewer') and review.reviewer == user:
        return True
      if hasattr(review, 'reviewee') and review.reviewee == user:
        return True

    if hasattr(obj, 'talk'):
      talk = obj.talk
      if hasattr(talk, 'participants') and user in talk.participants.all():
        return True

    if hasattr(obj, 'participants') and user in obj.participants.all():
      return True

    if hasattr(obj, 'content_object'):
      if self.has_object_permission(request, view, obj.content_object):
        return True

    return False
