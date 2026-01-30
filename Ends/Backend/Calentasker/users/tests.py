from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class UserModelTest(TestCase):
    def test_display_username_with_username(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        self.assertEqual(user.display_username, 'testuser')

    def test_display_username_without_username(self):
        user = User.objects.create(username=None, first_name='John', last_name='Doe', email='john@example.com')
        # Username is now auto-generated as First_Last
        self.assertEqual(user.display_username, 'John_Doe')

    def test_display_username_fallback_email(self):
        user = User.objects.create(username=None, first_name='', last_name='', email='fallback@example.com')
        self.assertEqual(user.display_username, 'fallback@example.com')

class UserSearchViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', email='specific@example.com', password='password')
        self.user2 = User.objects.create_user(username='other', email='other@example.com', first_name='Specific', password='password')
        self.client.force_authenticate(user=self.user1)

    def test_search_email_exact(self):
        response = self.client.get('/api/users/search/', {'q': 'specific@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should be first because exact email match
        self.assertEqual(response.data[0]['email'], 'specific@example.com')

    def test_search_partial(self):
        response = self.client.get('/api/users/search/', {'q': 'specific'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 2)
        # Verify ordering: user1 (email match) should be before user2 (name match)? 
        # Actually logic is: exact email (3) > contains email (2) > name/username (1)
        # 'specific' is in user1 email (contains -> 2)
        # 'specific' is user2 first name (relevance -> 1)
        # So user1 should be first.
        self.assertEqual(response.data[0]['id'], self.user1.id)

class UserUpdateTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='me', password='password')
        self.other_user = User.objects.create_user(username='other', password='password')
        self.client.force_authenticate(user=self.user)

    def test_update_self(self):
        url = f'/api/users/{self.user.id}/'
        response = self.client.patch(url, {'first_name': 'NewName'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NewName')

    def test_update_other_fails(self):
        url = f'/api/users/{self.other_user.id}/'
        response = self.client.patch(url, {'first_name': 'Hacked'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class UserCreationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_with_names_no_username(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'strongpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        # Assuming we have a registration endpoint or using UserSerializer directly
        # Since I don't know the exact registration URL, I will test the Serializer directly which is what the view uses.
        from .serializers import UserSerializer
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')
        # Expect generated username
        self.assertEqual(user.username, 'New_User')
        self.assertEqual(user.display_username, 'New_User')

    def test_update_user_clearing_username(self):
        user = User.objects.create_user(username='original', first_name='John', last_name='Doe', email='john@example.com', password='pass')
        user.username = ''
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.username, 'John_Doe')
