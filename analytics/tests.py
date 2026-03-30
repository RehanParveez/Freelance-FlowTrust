from django.test import TestCase
from accounts.models import User
from contracts.models import Contract
from analytics.models import UserAnalytics, ContractAnalytics, EarningReport
from milestones.models import Milestone
from payments.models import Escrow, Payment 
from accounts.tests import ParentTest

class AnalyticsSignalTest(TestCase):
  def setUp(self):
    self.client_user = User.objects.create_user(username = 'client', email = 'client@gmail.com', control = 'client')
    self.freelancer_user = User.objects.create_user(username = 'freelancer', email = 'freelancer@gmail.com', control = 'freelancer')
    self.contract = Contract.objects.create(client=self.client_user, freelancer=self.freelancer_user, title = 'contract test', status = 'active', total_amount=4500)

  def test_contr_created(self):
    client_anal = UserAnalytics.objects.get(user=self.client_user)
    freel_anal = UserAnalytics.objects.get(user=self.freelancer_user)
    self.assertEqual(client_anal.total_contr, 1)
    self.assertEqual(freel_anal.total_contr, 1)

  def test_contr_completed(self):
    self.contract.status = 'completed'
    self.contract.save()
    client_anal = UserAnalytics.objects.get(user=self.client_user)
    freel_anal = UserAnalytics.objects.get(user=self.freelancer_user)
    self.assertEqual(client_anal.completed_contr, 1)
    self.assertEqual(freel_anal.completed_contr, 1)

  def test_milestone(self):
    milest = Milestone.objects.create(contract=self.contract, title = 'milestone 1', status = 'pending', amount=2000)
    contr_anal = ContractAnalytics.objects.get(contract=self.contract)
    self.assertEqual(contr_anal.total_milest, 1)
    milest.status = 'approved'
    milest.save()
    contr_anal.refresh_from_db()
    self.assertEqual(contr_anal.milest_completed, 1)

  def test_payment(self):
    milestone = Milestone.objects.create(contract=self.contract, title = 'milestone 1', status = 'approved', amount=2000)
    escrow = Escrow.objects.create(milestone=milestone, amount=4500, client=self.client_user, freelancer=self.freelancer_user)
    payment = Payment.objects.create(escrow=escrow, client=self.client_user, freelancer=self.freelancer_user, amount=4500)
        
    user_anal = UserAnalytics.objects.get(user=self.freelancer_user)
    contr_anal = ContractAnalytics.objects.get(contract=self.contract)
    earn_report = EarningReport.objects.filter(user=self.freelancer_user, contract=self.contract)
    earn_report = earn_report.first()
    self.assertEqual(user_anal.total_earnings, 4500)
    self.assertEqual(contr_anal.total_pay, 4500)
    self.assertIsNotNone(earn_report)
    self.assertEqual(earn_report.amount, 4500)
    
class AnalyticsAPITest(ParentTest):
  def setUp(self):
    super().setUp()  
    self.auth_user(self.client1)
    self.contract = Contract.objects.create(client=self.client1, freelancer=self.freelancer1, title = 'contract test', total_amount=45000, status = 'active')
    self.milestone = Milestone.objects.create(contract=self.contract, title = 'milestone 1', amount=25000, order=1, status = 'approved', is_approved=True)
    self.escrow = Escrow.objects.create(milestone=self.milestone, client=self.client1, freelancer=self.freelancer1, amount=25000, is_funded=True, is_released=True)
    self.payment = Payment.objects.create(escrow=self.escrow, client=self.client1, freelancer=self.freelancer1, amount=25000)
    self.user_analytics, created = UserAnalytics.objects.get_or_create(user=self.client1, defaults={'total_contr': 1, 'completed_contr': 1, 'total_earnings': 45000})
    self.contract_analytics, created = ContractAnalytics.objects.get_or_create(contract=self.contract, defaults={'total_milest': 1, 'milest_completed': 1, 'total_pay': 10000})
    self.earning_report = EarningReport.objects.create(user=self.freelancer1, contract=self.contract, amount=12000)

  def test_user_analy1(self):
    url = '/analytics/useranaly/'
    res = self.client.get(url)

    self.assertEqual(res.status_code, 200)
    self.assertIn('total_contracts', res.data)
    self.assertIn('completed_contracts', res.data)
    self.assertIn('total_earnings', res.data)
    self.assertIn('average_earning', res.data)

  def test_contr_analy1(self):
    url = f'/analytics/contractanaly/{self.contract.id}/'
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.data['total_milestones'], 1)

  def test_contr_analy2(self):
    other_user = User.objects.create_user(username = 'other', email = 'other@gmail.com', password = 'oth123456', control = 'client')
    self.auth_user(other_user)
    url = f'/analytics/contractanaly/{self.contract.id}/'
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 403)

  def test_earnings(self):
    self.auth_user(self.freelancer1)
    url = '/analytics/earningsview/'
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 200)
    self.assertTrue(isinstance(resp.data, list))

  def test_dashboard(self):
    url = '/analytics/dashboardview/'
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 200)
    self.assertIn('user_data', resp.data)
    self.assertIn('milest_completed', resp.data)

  def test_user_analy2(self):
    new_user = User.objects.create_user(username = 'newuser', email = 'new@gmail.com', password = 'new123456', control = 'client')
    self.auth_user(new_user)
    url = '/analytics/useranaly/'
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 200)
    self.assertEqual(resp.data['total_contracts'], 0)
