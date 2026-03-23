from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

# Create your tests here.
class ParentTest(TestCase):
  def setUp(self):
    User = get_user_model()
    self.admin = User.objects.create_superuser(username = 'admin', password = 'adm12312', email = 'admin@gmail.com')
    self.client1 = User.objects.create_user(username = 'client1', password = 'cli12312', email = 'client@gmail.com', control = 'client')
    self.freelancer1 = User.objects.create_user(username = 'freelancer1', password = 'free12312', email = 'freelancer1@gmail.com', control = 'freelancer')
    self.freelancer2 = User.objects.create_user(username = 'freelancer2', password = 'free12312', email = 'freelancer2@gmail.com', control = 'freelancer')
    self.client = APIClient()
    
  def auth_user(self, user):
    self.client.force_authenticate(user=user)

class AuthTest(ParentTest):
  def test_check(self):
    self.assertEqual(self.admin.username, 'admin')
    self.assertEqual(self.client1.username, 'client1')
    self.assertEqual(self.freelancer1.username, 'freelancer1')
    self.assertEqual(self.freelancer2.username, 'freelancer2')
