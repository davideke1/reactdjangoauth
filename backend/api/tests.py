from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import UserProfile

User = get_user_model()

class UserModelTestCase(TestCase):
    print(User)
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )

    def test_user_model_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpassword'))
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_admin)

    def test_user_model_full_name(self):
        self.assertEqual(self.user.get_full_name(), 'John Doe')

    def test_user_profile_creation(self):
        profile = UserProfile.objects.create(
            user=self.user,
            gender='M',
            mobile_number='1234567890'
        )

        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.gender, 'M')
        self.assertEqual(profile.mobile_number, '1234567890')

class UserProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            gender='M',
            mobile_number='1234567890'
        )

    def test_user_profile_model_str(self):
        self.assertEqual(str(self.profile), 'testuser')

    def test_user_profile_model_fields(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.gender, 'M')
        self.assertEqual(self.profile.mobile_number, '1234567890')
