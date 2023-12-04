"""
Test for the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# APIClient is a test client that allows us to make requests to our API and check the response
from rest_framework.test import APIClient
# status is a module that contains some status codes that we can use when returning responses from our API
from rest_framework import status

CREATE_USER_URL = reverse('user:create')    # user:create is the name of the URL
TOKEN_URL = reverse('user:token')   # user:token is the name of the URL
ME_URL = reverse('user:me')     # user:me is the name of the URL


def create_user(**params):
    """Helper function to create a user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests the users API (public)"""

    def setUp(self):
        """Set up the test client"""
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating user is successful"""
        # Create a payload
        payload = {
            'email': 'test@example.com',
            'password': 'Testpass123',
            'name': 'Test name',
        }

        # Make an HTTP POST request to the URL

        res = self.client.post(CREATE_USER_URL, payload)

        # Check that the response is HTTP 201, standard API HTTP code for created objects in the database
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Check that the user was created correctly
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)    # Check that the password is not returned in the response

    def test_user_with_email_exists_errors(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'test@example.com',
            'password': 'Testpass123',
            'name': 'Test name',
        }

        # Create the user, because we are testing that the user already exists
        create_user(**payload)  # **payload is the same as email=payload['email'], password=payload['password'], name=payload['name']

        # Make an HTTP POST request to the URL

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_errors(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that the user was not created
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user_success(self):
        """Test that a token is created for the user"""
        user_details = {
            'email': 'test@example.com',
            'password': 'Testpass123',
            'name': 'Test name',
        }

        # Create the user
        create_user(**user_details)

        # Create a payload for the token
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        # Make an HTTP POST request to the URL

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials_errors(self):
        """Test that token is not created if invalid credentials are given"""
        user_details = {
            'email': 'test@example.com',
            'password': 'Testpass123',
            'name': 'Test name',
        }

        # Create the user
        create_user(**user_details)

        # Create a payload for the token
        payload = {
            'email': user_details['email'],
            'password': 'wrong_password',
        }

        # Make an HTTP POST request to the URL
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_blank_credentials_errors(self):
        """Test that token is not created if blank credentials are given"""
        user_details = {
            'email': 'test@example.com',
            'password': 'Testpass123',
            'name': 'Test name',
        }

        # Create the user
        create_user(**user_details)

        # Create a payload for the token
        payload = {
            'email': user_details['email'],
            'password': '',
        }

        # Make an HTTP POST request to the URL
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        # Make an HTTP GET request to the URL
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# We splitted the tests into two classes, one for the public API and one for the private API, so it's easier set the authentication in the SetUp function
# That way we don't have to set the authentication in every test function
class PrivateUserApiTests(TestCase):
    """Tests API requests that require authentication"""

    def setUp(self):
        """Set up the test client"""
        self.user_details = {
            'email': 'test@example.com',
            'password': 'Testpass123',
            'name': 'Test name',
        }

        self.user = create_user(**self.user_details)

        # DRF API test client that allows us to make authenticated requests
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        # Make an HTTP GET request to the URL
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # Check that the response data is the same as the user data
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed_errors(self):
        """Test that POST is not allowed on the me endpoint"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_success(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            'name': 'New name',
            'password': 'New password',
        }

        # Make an HTTP PATCH request to the URL
        res = self.client.patch(ME_URL, payload)

        # Refresh the user object from the database
        # Not refreshed automatically
        # We get the user when we do the first create_user, but we need to refresh it after we make the patch request
        self.user.refresh_from_db()

        # Check that the user name was updated correctly
        self.assertEqual(self.user.name, payload['name'])

        # Check that the user password was updated correctly
        self.assertTrue(self.user.check_password(payload['password']))

        # Check that the response is HTTP 200
        self.assertEqual(res.status_code, status.HTTP_200_OK)
