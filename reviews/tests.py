from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from contracts.models import Contract
from reviews.models import Review

class ReviewViewsetTest(APITestCase):
  def setUp(self):
    User = get_user_model()
    self.client_user = User.objects.create_user( username = 'client1', email = 'client@gmail.com', password = 'cli1123456', control = 'client')
    self.freelancer_user = User.objects.create_user(username = 'freelancer1', email = 'freelancer@gmail.com', password = 'freel1123456', control = 'freelancer')
    self.other_user = User.objects.create_user(username = 'other', email = 'other@gmail.com', password = 'other123456', control = 'client')
    self.contract = Contract.objects.create(client=self.client_user, freelancer=self.freelancer_user, title = 'the contract test', total_amount=1000, status = 'completed')
    self.url = '/reviews/review/'
    
  def test_create_review1(self):
    self.client.force_authenticate(user=self.client_user)
    data = {'contract': self.contract.id, 'comments': 'Great work'}
    res = self.client.post(self.url, data)
    self.assertEqual(res.status_code, 201)
    self.assertEqual(Review.objects.count(), 1)

    review = Review.objects.first()
    self.assertEqual(review.reviewer, self.client_user)
    self.assertEqual(review.reviewee, self.freelancer_user)

  def test_create_review2(self):
    self.client.force_authenticate(user=self.client_user)
    data = {'comments': 'Great work'}
    res = self.client.post(self.url, data)
    self.assertEqual(res.status_code, 400)

  def test_create_review3(self):
    self.client.force_authenticate(user=self.client_user)
    data = {'contract': 2000, 'comments': 'great work done'}
    res = self.client.post(self.url, data)
    self.assertEqual(res.status_code, 400)

  def test_create_review4(self):
    self.contract.status = 'active'
    self.contract.save()

    self.client.force_authenticate(user=self.client_user)
    data = {'contract': self.contract.id, 'comments': 'great work done'}
    res = self.client.post(self.url, data)
    self.assertEqual(res.status_code, 400)

  def test_create_review5(self):
    Review.objects.create(reviewer=self.client_user, reviewee=self.freelancer_user, contract=self.contract, comments = 'previous review')

    self.client.force_authenticate(user=self.client_user)
    data = {'contract': self.contract.id, 'comments': 'new review'}
    res = self.client.post(self.url, data)
    self.assertEqual(res.status_code, 400)

  def test_freel_review(self):
    self.client.force_authenticate(user=self.freelancer_user)
    data = {'contract': self.contract.id, 'comments': 'good client'}
    res = self.client.post(self.url, data)
    self.assertEqual(res.status_code, 201)
    
    review = Review.objects.first()
    self.assertEqual(review.reviewer, self.freelancer_user)
    self.assertEqual(review.reviewee, self.client_user)
  