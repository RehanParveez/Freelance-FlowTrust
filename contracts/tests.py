from accounts.tests import ParentTest
from contracts.models import Contract
from milestones.models import Milestone

# Create your tests here.
class ContractViewsetTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.contr = Contract.objects.create(client=self.client1, freelancer=self.freelancer1, title='contract test', total_amount=9000, status = 'draft')
    
  def test_add_milest1(self):
    self.auth_user(self.client1)
    url = f'/contracts/contract/{self.contr.id}/add_milest/'
    data = {'title': 'milestone add', 'status': 'pending', 'amount': 1500}
    resp = self.client.post(url, data, format='json')
    print(resp.data)
    self.assertEqual(resp.status_code, 201)
    
  def test_add_milest2(self):
    self.auth_user(self.freelancer1)
    url = f'/contracts/contract/{self.contr.id}/add_milest/'
    data = {'title': 'milestone', 'status': 'pending', 'amount': 2500}
    resp = self.client.post(url, data, format='json')
    self.assertEqual(resp.status_code, 403)
    
  def test_accept_contr1(self):
    self.contr.status = 'pending'
    self.contr.save()
    self.auth_user(self.freelancer1)
    
    url = f'/contracts/contract/{self.contr.id}/accept_contr/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    self.contr.refresh_from_db()
    self.assertEqual(self.contr.status, 'active')
  
  def test_accept_contr2(self):
    self.contr.status = 'pending'
    self.contr.save()
    self.auth_user(self.client1)
    url = f'/contracts/contract/{self.contr.id}/accept_contr/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 403)
    
  def test_accept_contr3(self):
    self.contr.status = 'pending'
    self.contr.save()
    self.auth_user(self.client1)
    url = f'/contracts/contract/{self.contr.id}/accept_contr/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 403)
  
  def test_complete_contr1(self):
    self.contr.status = 'active'
    self.contr.save()
    Milestone.objects.create(contract=self.contr, title = 'milest 1', amount=3000, is_approved=True)
    Milestone.objects.create(contract=self.contr, title ='milest 2', amount=6000, is_approved=True)

    self.auth_user(self.client1)
    url = f'/contracts/contract/{self.contr.id}/complete_contr/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    self.contr.refresh_from_db()
    self.assertEqual(self.contr.status, 'completed')
    
  def test_complete_contr2(self):
    self.contr.status = 'active'
    self.contr.save()
    Milestone.objects.create(contract=self.contr, title = 'milest 3', amount=3000, is_approved=True)
    Milestone.objects.create(contract=self.contr, title = 'milest 4', amount=6000, is_approved=False)

    self.auth_user(self.client1)
    url = f'/contracts/contract/{self.contr.id}/complete_contr/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 400)
    self.contr.refresh_from_db()
    self.assertNotEqual(self.contr.status, 'completed')

    self.auth_user(self.freelancer1)
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 403)