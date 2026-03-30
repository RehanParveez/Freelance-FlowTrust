from django.test import TestCase
from accounts.models import User
from contracts.models import Contract
from analytics.models import UserAnalytics, ContractAnalytics, EarningReport
from milestones.models import Milestone
from payments.models import Escrow, Payment 

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
