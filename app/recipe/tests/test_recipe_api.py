"""
Test for recipe API
"""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe

from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


# Helper function
def create_recipe(user, **params):
    """Create and return a sample recipe"""

    # Create a dictionary with the default values because we don't want to chnage the passes params, that can be used elsewhere
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 22,
        'price': Decimal('5.00'),
        'description': 'Sample description',
        'link': 'https://sample.com/recipe',

    }

    # The update function is a function that comes with the dictionary
    # The update function is a function that updates the dictionary with the values from the params
    # The update function is a function that updates the dictionary with the values from the params, but only if the key does not exist in the dictionary
    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)

    return recipe


class PublicRecipeAPITest(TestCase):
    """Test unauthenticated recipe API access"""

    def SetUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITest(TestCase):
    """Test authenticated recipe API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        # -id is used to order in reversed order, most recent first
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)   # many=True because we are serializing a list of objects

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes for user"""
        other_user = get_user_model().objects.create_user(
            'other_user@example.com'
            'testpass123',
        )

        create_recipe(user=other_user)
        create_recipe(user=self.user)   # The user that is authenticated

        res = self.client.get(RECIPES_URL)  # Should return only the recipe that is created by the authenticated user

        recipes = Recipe.objects.filter(user=self.user)     # Retrieve the recipes from the database that are created by the authenticated user
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)




