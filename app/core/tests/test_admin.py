"""
Test from the Django admin modification
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin"""

    def setUp(self):
        """Create user and client"""

        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@examples.com',
            password='Testpass123',)

        # Log the admin user in with the Django authentication
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@eample.com',
            password='Testpass123',
            name='Test user',
        )

    def test_users_list(self):
        """Test that users are listed on user page"""
        # Generate the URL for the list user page
        # 'admin:core_user_changelist' is the Django admin page for listing users
        url = reverse('admin:core_user_changelist')
        # Use the test client to perform a HTTP GET on the URL
        res = self.client.get(url)

        # AssertContains checks that the response contains a certain item
        # Checks that the response is HTTP 200
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test that the edit user page works"""
        # Generate the URL for the edit user page
        # 'admin:core_user_change' is the Django admin page for editing users
        url = reverse('admin:core_user_change', args=[self.user.id])
        # Use the test client to perform a HTTP GET on the URL
        res = self.client.get(url)

        # Checks that the response is HTTP 200
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        # Generate the URL for the create user page
        # 'admin:core_user_add' is the Django admin page for creating users
        url = reverse('admin:core_user_add')
        # Use the test client to perform a HTTP GET on the URL
        res = self.client.get(url)

        # Checks that the response is HTTP 200
        self.assertEqual(res.status_code, 200)
