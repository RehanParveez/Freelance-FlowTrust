from accounts.tests import ParentTest
from contracts.models import Contract
from milestones.models import Milestone
from payments.models import Wallet, Escrow, Payment

class PaymentViewsetTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.contr = Contract.objects.create(client=self.client1, freelancer=self.freelancer1, title = 'contract test', total_amount=11000) 
    self.milest = Milestone.objects.create(contract=self.contr, title = 'milestone test', status = 'pending', amount=4000)  
    self.wallet = Wallet.objects.create(user=self.client1, balance=11000)
    
  def test_deposit1(self):
    self.auth_user(self.client1)
    url = f'/payments/payment/{self.milest.id}/deposit/'
    data = {'amount': 2000}
    resp = self.client.post(url, data, format='json')
    self.assertEqual(resp.status_code, 200)
    escrow = Escrow.objects.filter(milestone=self.milest)
    escrow = escrow.first()
    self.assertIsNotNone(escrow)
    self.assertTrue(escrow.is_funded)
    
    self.wallet.refresh_from_db()
    self.assertEqual(self.wallet.balance, 9000)
  
  def test_deposit2(self):
    self.auth_user(self.freelancer1)
    url = f'/payments/payment/{self.milest.id}/deposit/'
    data = {'amount': 2000}
    resp = self.client.post(url, data, format='json')
    self.assertEqual(resp.status_code, 403)
    
  def test_wallet(self):
    self.auth_user(self.client1)
    url = '/payments/payment/wallet/'
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 200)
    self.assertIn('balance', resp.data)
  
  def test_refund1(self):
    self.auth_user(self.client1)
    self.client.post(f'/payments/payment/{self.milest.id}/deposit/', {'amount': 2000}, format='json')
    escrow = Escrow.objects.get(milestone=self.milest)
    payment = Payment.objects.create(escrow=escrow, client=self.client1, freelancer=self.freelancer1, amount=escrow.amount)
    url = f'/payments/payment/{payment.id}/refund/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)

    self.wallet.refresh_from_db()
    self.assertEqual(self.wallet.balance, 11000)
    self.assertFalse(Escrow.objects.filter(id=escrow.id).exists())
  
  def test_refund2(self):
    self.auth_user(self.client1)
    self.client.post(f'/payments/payment/{self.milest.id}/deposit/', {'amount': 2000}, format='json')
    escrow = Escrow.objects.get(milestone=self.milest)
    escrow.is_released = True
    escrow.save()
    payment = Payment.objects.create(escrow=escrow, client=self.client1, freelancer=self.freelancer1, amount=escrow.amount)
    
    url = f'/payments/payment/{payment.id}/refund/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 400)
    