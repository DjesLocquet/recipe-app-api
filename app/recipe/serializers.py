"""
Serializers for recipe API.
"""

from rest_framework import serializers

from core.models import Recipe


# Using the ModelSerializer because we will be working with model objects Recipe
class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = Recipe
        fields = [
            'id',
            'title',
            'time_minutes',
            'price',
            'link'
        ]
        read_only_fields = ['id']   # The id is automatically assigned by Django, so we don't want to allow the user to change it


# RecipeDetailSerializer inherits from RecipeSerializer because this is an extension of the RecipeSerializer
# We want all the same functionality as the RecipeSerializer and we want to add some additional fields
class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
