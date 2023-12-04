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

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer

RECIPES_URL = reverse('recipe:recipe-list')


# Helper function
def detail_url(recipe_id):
    """Return recipe detail URL"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


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


def create_user(**params):
    """Create and return a sample user"""
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(email='user@example.com', password='testpass123')

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
        other_user = create_user(email='other_user@example.com', password='testpass123')

        create_recipe(user=other_user)
        create_recipe(user=self.user)   # The user that is authenticated

        res = self.client.get(RECIPES_URL)  # Should return only the recipe that is created by the authenticated user

        recipes = Recipe.objects.filter(user=self.user)     # Retrieve the recipes from the database that are created by the authenticated user
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_recipe_detail(self):
        """Test viewing a recipe detail"""
        recipe = create_recipe(user=self.user)

        # Generate the url for the recipe detail
        url = detail_url(recipe.id)

        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)

        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a new recipe using the API"""
        payload = {
            'title': 'Chocolate cheesecake',
            'time_minutes': 30,
            'price': Decimal('5.99'),
        }

        res = self.client.post(RECIPES_URL, payload)    # Post the payload to the RECIPES_URL /api/recipes/recipe

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)  # Check if the status code is 201 CREATED   # 201 is the standard HTTP status code for created

        # Retrieve the recipe from the database
        recipe = Recipe.objects.get(id=res.data['id'])

        # Loop through the payload and check if the values are the same
        for k, v in payload.items():
            self.assertEqual(v, getattr(recipe, k))

        self.assertEqual(recipe.user, self.user)

    def test_partial_update(self):
        """Test partial update of a recipe using the API"""
        original_link = 'https://original.com/recipe.pdf'
        recipe = create_recipe(
                            user=self.user,
                            title='Original title',
                            link=original_link,
                               )

        payload = {'title': 'Updated title'}
        url = detail_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()    # Refresh the recipe from the database

        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.user, self.user)

    def test_full_update(self):
        """Test full update of a recipe using the API"""
        recipe = create_recipe(
            user=self.user,
            title='Original title',
            link='https://original.com/recipe.pdf',
            description='Original description',
        )

        payload = {
            'title': 'Updated title',
            'link': 'https://updated.com/recipe.pdf',
            'description': 'Updated description',
            'time_minutes': 25,
            'price': Decimal('10.00'),
        }

        url = detail_url(recipe.id)
        res = self.client.put(url, payload)     # Put the payload to the url, full update

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()

        for k, v in payload.items():
            self.assertEqual(v, getattr(recipe, k))

        self.assertEqual(recipe.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the recipe user results in error"""
        new_user = create_user(email='new_user@example.com', password='testpass123')
        recipe = create_recipe(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(recipe.id)

        res = self.client.patch(url, payload)

        recipe.refresh_from_db()

        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Test deleting a recipe using the API"""
        recipe = create_recipe(user=self.user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)   # 204 is the standard HTTP status code for no content, when we delete something

        # Check if the recipe is deleted from the database
        exists = Recipe.objects.filter(id=recipe.id).exists()

        self.assertFalse(exists)

    def test_recipe_other_users_recipe_error(self):
        """Test that other users can't delete recipes"""
        other_user = create_user(email='other_user@example.com', password='testpass123')
        recipe = create_recipe(user=other_user)

        url = detail_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
