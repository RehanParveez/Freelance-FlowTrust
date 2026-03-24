from accounts.tests import ParentTest
from contracts.models import Contract
from milestones.models import Milestone
from payments.models import Escrow, Payment, Wallet

# Create your tests here.
class MilestoneViewsetTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.contr = Contract.objects.create(client=self.client1, freelancer=self.freelancer1, title = 'contract test', total_amount=7000)
    self.milest1 = Milestone.objects.create(contract=self.contr, title = 'milest1', status = 'pending', amount=2000)
    self.milest2 = Milestone.objects.create(contract=self.contr, title = 'milest2', status = 'submitted', amount=3000)
    self.escrow2 = Escrow.objects.create(milestone=self.milest2, client=self.client1, freelancer=self.freelancer1, amount=self.milest2.amount, is_funded=False, is_released=False)
    self.wallet_client = Wallet.objects.create(user=self.client1, balance=7000)
    self.wallet_freelancer = Wallet.objects.create(user=self.freelancer1, balance=0)
  
  def test_sub_milest1(self):
    self.auth_user(self.freelancer1)
    url = f'/milestones/milestone/{self.milest1.id}/sub_milest/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    
  def test_sub_milest2(self):
    self.auth_user(self.client1)  
    url = f'/milestones/milestone/{self.milest1.id}/sub_milest/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 403)
    
  def test_approve_milest1(self):
    self.milest2.status = 'submitted'
    self.milest2.save()
    escrow = self.escrow2
    escrow.is_funded = True
    escrow.save()
    self.auth_user(self.client1)
    url = f'/milestones/milestone/{self.milest2.id}/approve_milest/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(Payment.objects.filter(escrow=escrow).exists())

    self.freelancer1.wallet.refresh_from_db()
    self.assertEqual(self.freelancer1.wallet.balance, escrow.amount)
    escrow.refresh_from_db()
    self.assertTrue(escrow.is_released)
    
  def test_approve_milest2(self):
    self.milest2.status = 'submitted'
    self.milest2.save()
    escrow = self.escrow2
    escrow.is_funded = True
    escrow.save()
    self.auth_user(self.freelancer1)
    
    url = f'/milestones/milestone/{self.milest2.id}/approve_milest/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 403)
    self.assertFalse(Payment.objects.filter(escrow=escrow).exists())
    self.freelancer1.wallet.refresh_from_db()
    self.assertEqual(self.freelancer1.wallet.balance, 0)
    escrow.refresh_from_db()
    self.assertFalse(escrow.is_released)
  
  def test_reject_milest(self):
    self.auth_user(self.freelancer1)
    url = f'/milestones/milestone/{self.milest2.id}/reject_miles/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 403)

    
  