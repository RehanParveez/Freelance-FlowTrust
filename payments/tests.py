from accounts.tests import ParentTest
from contracts.models import Contract
from milestones.models import Milestone
from payments.models import Escrow, Payment
from django.test import TestCase
from unittest.mock import patch
from accounts.models import User
from rest_framework.test import APITestCase

class PaymentViewsetTest(ParentTest):
  def setUp(self):
    super().setUp()
    self.contr = Contract.objects.create(client=self.client1, freelancer=self.freelancer1, title = 'contract test', total_amount=11000) 
    self.milest = Milestone.objects.create(contract=self.contr, title = 'milestone test', status = 'pending', amount=4000)  
    self.wallet = self.client1.wallet
    self.wallet.balance = 11000
    self.wallet.save()
    
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
    
class PaymentSignalTest(TestCase):
  @patch('core.tasks.send_notification.delay')
  def test_pay_relsignal(self, mock_send):
    client = User.objects.create_user(username = 'client', email = 'client@gmail.com', control = 'client')
    freelancer = User.objects.create_user(username = 'freelancer', email = 'freelancer@gmail.com', control = 'freelancer')
    contract = Contract.objects.create(client=client, freelancer=freelancer, title = 'C1', status='active', total_amount=10000)
    milestone = Milestone.objects.create(contract=contract, title = 'M1', amount=5000, status = 'approved')
    escrow = Escrow.objects.create(milestone=milestone, client=client, freelancer=freelancer, amount=5000, is_funded=True)
    payment = Payment.objects.create(escrow=escrow, client=client, freelancer=freelancer, amount=5000)
        
    mock_send.assert_called_once_with(
      subject='the payment is released',
      message=f'{payment.amount}',
      recipient_email=freelancer.email)
  
class FullFlowTest(APITestCase):
  def setUp(self):
    self.client1 = User.objects.create_user(username = 'client1', email = 'client1@gmail.com', control = 'client')
    self.freelancer1 = User.objects.create_user(username = 'freelancer1', email = 'freelancer1@gmail.com', control = 'freelancer')

  def auth_user(self, user):
    self.client.force_authenticate(user=user)

  @patch('payments.signals.send_notification.delay')
  def test_full(self, mock_send):
    self.auth_user(self.client1)
    contr = Contract.objects.create(client=self.client1, freelancer=self.freelancer1, title='contract test', total_amount=5000, status = 'pending')
    
    self.auth_user(self.freelancer1)
    res = self.client.post(f'/contracts/contract/{contr.id}/accept_contr/')
    self.assertEqual(res.status_code, 200)
    contr.refresh_from_db()
    self.assertEqual(contr.status, 'active')

    self.auth_user(self.client1)
    res = self.client.post(f'/contracts/contract/{contr.id}/add_milest/', {'title': 'milest1', 'amount': 2000})
    self.assertEqual(res.status_code, 201)
    milest = Milestone.objects.get(contract=contr)
    self.client1.wallet.balance = 5000
    self.client1.wallet.save()
    res = self.client.post( f'/payments/payment/{milest.id}/deposit/', {'amount': 2000})
    self.assertEqual(res.status_code, 200)
    escrow = Escrow.objects.get(milestone=milest)
    
    self.auth_user(self.freelancer1)
    res = self.client.post(f'/milestones/milestone/{milest.id}/sub_milest/')
    self.assertEqual(res.status_code, 200)
    milest.refresh_from_db()
    self.assertEqual(milest.status, 'submitted')

    self.auth_user(self.client1)
    res = self.client.post(f'/milestones/milestone/{milest.id}/approve_milest/')
    self.assertEqual(res.status_code, 200)
    self.assertTrue(Payment.objects.filter(escrow=escrow).exists())
    
    self.freelancer1.wallet.refresh_from_db()
    self.assertEqual(self.freelancer1.wallet.balance, 2000)
    contr.refresh_from_db()
    self.assertEqual(contr.status, 'completed')
    self.assertTrue(mock_send.called)