from accounts.tests import ParentTest
from contracts.models import Contract
from milestones.models import Milestone
from payments.models import Escrow

# Create your tests here.
class MilestoneViewsetTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.contr = Contract.objects.create(client=self.client1, freelancer=self.freelancer1, title = 'contract test', total_amount=7000)
    self.milest1 = Milestone.objects.create(contract=self.contr, title = 'milest1', status = 'pending', amount=2000)
    self.milest2 = Milestone.objects.create(contract=self.contr, title = 'milest2', status = 'submitted', amount=3000)
    self.escrow2 = Escrow.objects.create(milestone=self.milest2, client=self.client1, freelancer=self.freelancer1, amount=self.milest2.amount, is_funded=False, is_released=False)
  
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
    self.milest2.escrow.is_funded = True
    self.milest2.escrow.save()
    self.auth_user(self.client1)
    url = f'/milestones/milestone/{self.milest2.id}/approve_milest/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    
  def test_approve_milest2(self):
    self.milest2.escrow.is_funded = True
    self.milest2.escrow.save()
    self.auth_user(self.freelancer1)
    url = f'/milestones/milestone/{self.milest2.id}/approve_milest/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 403)
  
  def test_reject_milest(self):
    self.auth_user(self.freelancer1)
    url = f'/milestones/milestone/{self.milest2.id}/reject_miles/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 403)

    
  