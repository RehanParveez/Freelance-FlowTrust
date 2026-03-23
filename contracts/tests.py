from accounts.tests import ParentTest
from contracts.models import Contract

# Create your tests here.
class ContractViewsetTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.contr = Contract.objects.create(client=self.client1, freelancer=self.freelancer1, title='contract test', total_amount=9000)
    
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