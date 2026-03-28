from django.test import TestCase
from rest_framework.test import APIClient
from accounts.models import User
from contracts.models import Contract
from decimal import Decimal
from milestones.models import Milestone
from disputes.models import Dispute, DisputeMessage, Solution
from payments.models import Wallet, Escrow

class DisputeViewsetTest(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.admin = User.objects.create_user(username = 'admin', email = 'admin@gmail.com', control = 'admin')
    self.client_user = User.objects.create_user(username = 'client', email = 'client@gmail.com', control = 'client')
    self.freelancer = User.objects.create_user(username = 'freelancer', email = 'freelancer@gmail.com', control = 'freelancer')
    self.other = User.objects.create_user(username = 'other', email = 'other@gmail.com', control = 'freelancer')

    self.contract = Contract.objects.create(client=self.client_user, freelancer=self.freelancer, title = 'the contract test', total_amount=Decimal('3000.00'))
    self.milestone = Milestone.objects.create(contract=self.contract, amount=Decimal('3000.00'), status = 'pending')
    self.dispute = Dispute.objects.create(contract=self.contract, milestone=self.milestone, raised_by=self.client_user, description = 'Issue')
    
    client_wallet = Wallet.objects.get(user=self.client_user)
    client_wallet.balance = Decimal('0')
    client_wallet.save()
    
    freelancer_wallet = Wallet.objects.get(user=self.freelancer)
    freelancer_wallet.balance = Decimal('0')
    freelancer_wallet.save()
    self.escrow = Escrow.objects.create(milestone=self.milestone, client=self.client_user, freelancer=self.freelancer, amount=Decimal('3000.00'), is_funded=True)

  def test_submit_proof1(self):
    self.client.force_authenticate(user=self.client_user)

    url = f'/disputes/dispute/{self.dispute.id}/submit_proof/'
    res = self.client.post(url, {'content': 'the text of proof'})
    self.assertEqual(res.status_code, 200)
    self.dispute.refresh_from_db()
    
    self.assertEqual(self.dispute.status, 'checking')
    self.assertTrue(DisputeMessage.objects.filter(dispute=self.dispute).exists())

  def test_submit_proof2(self):
    self.client.force_authenticate(user=self.other)
    
    url = f'/disputes/dispute/{self.dispute.id}/submit_proof/'
    res = self.client.post(url, {'content': 'checking test'})
    self.assertEqual(res.status_code, 404)

  def test_solve_dispute1(self):
    self.client.force_authenticate(user=self.admin)
    
    url = f'/disputes/dispute/{self.dispute.id}/solve_dispute/'
    res = self.client.post(url, {'amount_rel_to_freel': '2000', 'amount_ref_to_client': '1000'})
    self.assertEqual(res.status_code, 200)
    self.dispute.refresh_from_db()
    self.assertEqual(self.dispute.status, 'solved')
    self.escrow.refresh_from_db()
    
    self.assertTrue(self.escrow.is_released)
    self.assertTrue(Solution.objects.filter(dispute=self.dispute).exists())

  def test_solve_dispute2(self):
    self.client.force_authenticate(user=self.client_user)

    url = f'/disputes/dispute/{self.dispute.id}/solve_dispute/'
    res = self.client.post(url, {'amount_rel_to_freel': '1000'})
    self.assertEqual(res.status_code, 403)

  def test_solve_dispute3(self):
    self.client.force_authenticate(user=self.admin)

    url = f'/disputes/dispute/{self.dispute.id}/solve_dispute/'
    res = self.client.post(url, {'amount_rel_to_freel': '2500', 'amount_ref_to_client': '1000'})
    self.assertEqual(res.status_code, 400)

  def test_close_dispute(self):
    self.client.force_authenticate(user=self.admin)
    self.client.post(f'/disputes/dispute/{self.dispute.id}/solve_dispute/', {'amount_rel_to_freel': '1000', 'amount_ref_to_client': '2000'})
    self.client.force_authenticate(user=self.client_user)
    res = self.client.post(f'/disputes/dispute/{self.dispute.id}/close_dispute/')
    self.assertEqual(res.status_code, 200)

    self.dispute.refresh_from_db()
    self.assertEqual(self.dispute.status, 'closed')

  def test_close_dispute2(self):
    self.client.force_authenticate(user=self.client_user)
    res = self.client.post(f'/disputes/dispute/{self.dispute.id}/close_dispute/')
    self.assertEqual(res.status_code, 400)
