"""
URL mapping for the recipe app.
"""

from django.urls import path, include

# The DefaultRouter is a feature of the Django REST Framework that automatically generates the URLs for our viewset
from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),  # The router.urls is a function that returns a list of urls for our viewset
]
