from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """User model tests"""
    def test_create_user_with_email(self):
        """Test creating a new user with an email"""
        email = "user@user.com"
        password = "userpassword"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.password, password)
    
    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "user@USER.com"
        user = get_user_model().objects.create_user(email, 'userpassword')

        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        """Test creating an user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'userpassword')
    
    def test_create_new_superuser(self):
        """Test creatign a new superuser"""
        user = get_user_model().objects.create_superuser(
            email='superuser@superuser.com',
            password='superuserpassword'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
    
    def test_user_can_be_superhost(self):
        """Test user can become superhost"""
        user = get_user_model().objects.create(
            email='user@user.com',
            password='userpassword123'
        )
        user.superhost = True
        self.assertTrue(user.superhost)