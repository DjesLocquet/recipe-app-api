"""
Views for the Recipe API.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


# Using the ModelViewSet because we will be working with model objects Recipe and we want to allow all the CRUD operations
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipes API's"""

    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()     # The queryset is the objects that are managed by the viewset
    authentication_classes = [TokenAuthentication]  # The authentication_classes is the authentication classes that are used by the viewset
    permission_classes = [IsAuthenticated]  # The permission_classes is the permission classes that are used by the viewset

    # Override the get_queryset function to return recipes for the authenticated user only
    # Default function returns all the objects
    def get_queryset(self):
        """Return recipes for the authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return serializer class for requests"""
        # Return a reference to the serializer class not an instance of the serializer class!
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    # Override the perform_create function to add the authenticated user to the recipe
    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
