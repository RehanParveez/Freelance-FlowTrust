from django.test import TestCase
from rest_framework.test import APIRequestFactory
from accounts.models import User, Profile, VerificationStatus
from marketplace.models import FreelancerProfile, JobPost, Proposal
from contracts.models import Contract, ContrParticipant, ContractTerm, ContractStatus, Activity
from core.permissions import AdminPermission, ClientPermission, OwnerOrAdminPermission, ParticipantOrAdminPermission
from milestones.models import Milestone, MilestoneSubmission, MilestoneReview, MilestoneStatus
from communication.models import Talk, Message
from disputes.models import Dispute, DisputeMessage, Proof
from payments.models import Escrow, Payment, PaymentMethod, Refund, Transaction
from reviews.models import Review, Rating
from notifications.models import Notification
from analytics.models import UserAnalytics, EarningReport, ContractAnalytics

class PermissionTests(TestCase):
  def setUp(self):
   self.admin_user = User.objects.create_user(username = 'admin', email = 'admin@gmail.com', control = 'admin', password = 'admin123456')
   self.client_user = User.objects.create_user(username = 'client', email = 'client@gmail.com', control = 'client', password = 'cli123456')
   self.freelancer_user = User.objects.create_user(username = 'freelancer', email ='freelancer@gmail.com', control ='freelancer', password ='free123456')
   self.freelancer_profile = FreelancerProfile.objects.create(user=self.freelancer_user)
   self.contract = Contract.objects.create(client=self.client_user, freelancer=self.freelancer_user, title = 'contract test', total_amount=1000)
   self.job = JobPost.objects.create(client=self.client_user, name = 'job test', budget=500)
   self.proposal = Proposal.objects.create(job=self.job, freelancer=self.freelancer_profile, proposed_amount=1500)
   self.milestone = Milestone.objects.create(contract=self.contract, title ='milestone 1', amount=500, order=1)
   self.talk = Talk.objects.create(contract=self.contract)
   self.talk.participants.add(self.client_user, self.freelancer_user)
   self.message = Message.objects.create(talk=self.talk, by=self.freelancer_user, content = 'message test')

   self.factory = APIRequestFactory()

  def test_admin_permission(self):
    permission = AdminPermission()
    request = self.factory.get('/practice-url/')
    request.user = self.admin_user
    self.assertTrue(permission.has_permission(request, None))
    self.assertTrue(permission.has_object_permission(request, None, self.contract))

    request.user = self.client_user
    self.assertFalse(permission.has_permission(request, None))
    self.assertFalse(permission.has_object_permission(request, None, self.contract))

    request.user = self.freelancer_user
    self.assertFalse(permission.has_permission(request, None))
    self.assertFalse(permission.has_object_permission(request, None, self.contract))
        
  def test_client_permission(self):
    permission = ClientPermission()
    request = self.factory.get('/practice-url/')
    request.user = self.client_user
    self.assertTrue(permission.has_permission(request, None))
    self.assertTrue(permission.has_object_permission(request, None, self.contract))
    self.assertTrue(permission.has_object_permission(request, None, self.proposal))
    
    request.user = self.admin_user
    self.assertFalse(permission.has_permission(request, None))
    self.assertFalse(permission.has_object_permission(request, None, self.contract))
    self.assertFalse(permission.has_object_permission(request, None, self.proposal))
    
    request.user = self.freelancer_user
    self.assertFalse(permission.has_permission(request, None))
    self.assertFalse(permission.has_object_permission(request, None, self.contract))
    self.assertFalse(permission.has_object_permission(request, None, self.proposal))
    
  def test_freelancer_permission(self):
    from core.permissions import FreelancerPermission
    permission = FreelancerPermission()
    request = self.factory.get('/practice-url/')
    request.user = self.freelancer_user
    self.assertTrue(permission.has_permission(request, None))
    self.assertTrue(permission.has_object_permission(request, None, self.contract))
    self.assertTrue(permission.has_object_permission(request, None, self.proposal))
    self.assertTrue(permission.has_object_permission(request, None, self.milestone))
    self.assertTrue(permission.has_object_permission(request, None, self.message))

    request.user = self.client_user
    self.assertFalse(permission.has_permission(request, None))
    self.assertFalse(permission.has_object_permission(request, None, self.contract))
    self.assertFalse(permission.has_object_permission(request, None, self.proposal))
    self.assertFalse(permission.has_object_permission(request, None, self.milestone))
    self.assertFalse(permission.has_object_permission(request, None, self.message))

    request.user = self.admin_user
    self.assertFalse(permission.has_permission(request, None))
    self.assertFalse(permission.has_object_permission(request, None, self.contract))
    self.assertFalse(permission.has_object_permission(request, None, self.proposal))
    self.assertFalse(permission.has_object_permission(request, None, self.milestone))
    self.assertFalse(permission.has_object_permission(request, None, self.message))
    
class OwnerOrAdminPermissionTests(TestCase):
  def setUp(self):
    self.admin_user = User.objects.create_user(username = 'admin', email = 'admin@gmail.com', control = 'admin', password = 'admin123456')
    self.client_user = User.objects.create_user(username = 'client', email = 'client@gmail.com', control='client', password = 'cli123456')
    self.freelancer_user = User.objects.create_user(username = 'freelancer', email = 'freelancer@gmail.com', control = 'freelancer', password = 'free123456')
    self.freelancer_profile = FreelancerProfile.objects.create(user=self.freelancer_user)

    self.contract = Contract.objects.create(client=self.client_user, freelancer=self.freelancer_user, title = 'contract test', total_amount=1000)
    self.participant = ContrParticipant.objects.create(contract=self.contract, user=self.freelancer_user, role = 'freelancer')
    self.term = ContractTerm.objects.create(contract=self.contract, description = 'the term test')
    self.contract_status = ContractStatus.objects.create(contract=self.contract, prev_status = 'draft', new_status = 'pending', changed_by=self.client_user)
    self.activity = Activity.objects.create(user=self.client_user, action_type = 'the created contract', content_object=self.contract)

    self.milestone = Milestone.objects.create(contract=self.contract, title='milestone 1', amount=600)
    self.submission = MilestoneSubmission.objects.create(milestone=self.milestone, submitted_by=self.freelancer_user,  notes = 'submission')
    self.review = MilestoneReview.objects.create(submission=self.submission, reviewed_by=self.client_user)
    self.milestone_status = MilestoneStatus.objects.create(milestone=self.milestone, prev_status = 'pending', new_status = 'submitted', changed_by=self.freelancer_user)

    self.dispute = Dispute.objects.create(contract=self.contract, raised_by=self.client_user, description = 'the dispute')
    self.dispute_message = DisputeMessage.objects.create(dispute=self.dispute, by=self.client_user, content = 'the msg')
    self.proof = Proof.objects.create(dispute=self.dispute, file = 'proof file')

    self.wallet = self.client_user.wallet
    self.transaction = Transaction.objects.create(wallet=self.wallet, amount=100)
    self.escrow = Escrow.objects.create(milestone=self.milestone, client=self.client_user, freelancer=self.freelancer_user, amount=700)
    self.payment = Payment.objects.create(escrow=self.escrow, client=self.client_user, freelancer=self.freelancer_user, amount=700)
    self.refund = Refund.objects.create(payment=self.payment, amount=100, reason = 'the reason')
    self.payment_method = PaymentMethod.objects.create(user=self.client_user, method_type = 'card')

    self.job = JobPost.objects.create(client=self.client_user, name = 'this is a job', budget=500)
    self.proposal = Proposal.objects.create(job=self.job, freelancer=self.freelancer_profile, proposed_amount=400)

    self.profile = Profile.objects.create(user=self.client_user)
    self.ver_status = VerificationStatus.objects.create(user=self.client_user)

    self.review_model = Review.objects.create(reviewer=self.client_user, reviewee=self.freelancer_user)
    self.rating = Rating.objects.create(review=self.review_model, score=5)

    self.user_analytics = UserAnalytics.objects.create(user=self.client_user, total_contr=1, completed_contr=0, total_earnings=1000)
    self.earning_report = EarningReport.objects.create(user=self.client_user, contract=self.contract, amount=1000)
    self.contract_analytics = ContractAnalytics.objects.create(contract=self.contract, total_milest=1, milest_completed=0, total_pay=1000)

    self.notification = Notification.objects.create(user=self.client_user, content = 'this is anotification')

    self.talk = Talk.objects.create(contract=self.contract)
    self.talk.participants.add(self.client_user, self.freelancer_user)
    self.message = Message.objects.create(talk=self.talk, by=self.client_user, content = 'asalam alaikum')

    self.factory = APIRequestFactory()
    self.permission = OwnerOrAdminPermission()

  def all_perm(self, user):
    request = self.factory.get('/test/')
    request.user = user

    objects = [
      self.contract, self.participant, self.term, self.contract_status, self.activity, self.milestone, self.submission, self.review, self.milestone_status,
      self.dispute, self.dispute_message, self.proof, self.wallet, self.transaction, self.escrow, self.payment, self.refund, self.payment_method,
      self.job, self.proposal, self.profile, self.ver_status, self.review_model, self.rating, self.user_analytics, self.earning_report, self.contract_analytics,
      self.notification, self.talk, self.message]

    results = []
    for obj in objects:
      has_perm = self.permission.has_object_permission(request, None, obj)
      results.append((obj.__class__.__name__, has_perm))
    return results

  def test_admin_permissions(self):
    results = self.all_perm(self.admin_user)
    for name, perm in results:
      self.assertTrue(perm)

  def test_client_permissions(self):
    results = self.all_perm(self.client_user)
    for name, perm in results:
      if not perm:
        print(f'the permission is failing: {name}')
      self.assertTrue(perm)
      
class DummyTalk:
  def __init__(self, participants):
    self._participants = participants
    
  @property
  def participants(self):
     class Wrapper:
        def __init__(self, items):
          self._items = items
        def all(self):
          return self._items
     return Wrapper(self._participants)

class DummyMessage:
  def __init__(self, by, talk=None):
    self.by = by
    self.talk = talk

class DummyContract:
  def __init__(self, client, freelancer):
    self.client = client
    self.freelancer = freelancer

class DummyNegotiation:
  def __init__(self, contract):
    self.contract = contract

class ParticipantOrAdminPermissionTest(TestCase):
  def setUp(self):
    self.factory = APIRequestFactory()
    self.permission = ParticipantOrAdminPermission()
    self.admin = User.objects.create_user(username = 'admin', email = 'admin@gmail.com', password = 'admin123456', control = 'admin')
    self.client = User.objects.create_user(username = 'client', email = 'client@gmail.com', password = 'cli123456', control = 'client')
    self.freelancer = User.objects.create_user(username = 'freelancer', email = 'freelancer@gmail.com', password = 'free123456', control = 'freelancer')
    self.other_user = User.objects.create_user(username = 'other', email = 'other@gmail.com', password = 'other123456', control = 'freelancer')

  def test_admin_access(self):
    talk = DummyTalk(participants=[self.client])
    message = DummyMessage(by=self.client)
    contract = DummyContract(client=self.client, freelancer=self.freelancer)
    negotiation = DummyNegotiation(contract=contract)

    for obj in [talk, message, negotiation]:
      request = self.factory.get('/')
      request.user = self.admin
      self.assertTrue(self.permission.has_object_permission(request, None, obj))

  def test_talk_permissions(self):
    talk = DummyTalk(participants=[self.client, self.freelancer])
    request_client = self.factory.get('/')
    request_client.user = self.client
    request_other = self.factory.get('/')
    request_other.user = self.other_user
    self.assertTrue(self.permission.has_object_permission(request_client, None, talk))
    self.assertFalse(self.permission.has_object_permission(request_other, None, talk))

  def test_message_permissions(self):
    talk = DummyTalk(participants=[self.client, self.freelancer])
    message = DummyMessage(by=self.client, talk=talk)
    request_by = self.factory.post('/')
    request_by.user = self.client
    self.assertTrue(self.permission.has_object_permission(request_by, None, message))

    request_particip = self.factory.get('/')
    request_particip.user = self.freelancer
    self.assertTrue(self.permission.has_object_permission(request_particip, None, message))

    request_other = self.factory.get('/')
    request_other.user = self.other_user
    self.assertFalse(self.permission.has_object_permission(request_other, None, message))

  def test_negotiation_permissions(self):
    contract = DummyContract(client=self.client, freelancer=self.freelancer)
    negotiation = DummyNegotiation(contract=contract)

    request_client = self.factory.get('/')
    request_client.user = self.client
    request_freelancer = self.factory.get('/')
    request_freelancer.user = self.freelancer
    request_other = self.factory.get('/')
    request_other.user = self.other_user

    self.assertTrue(self.permission.has_object_permission(request_client, None, negotiation))
    self.assertTrue(self.permission.has_object_permission(request_freelancer, None, negotiation))
    self.assertFalse(self.permission.has_object_permission(request_other, None, negotiation))
