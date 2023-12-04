"""
Views for user API
"""

# rest_framework handles alot of the logic for creating objects in our database and it does that with different BaseClass views
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


# CreateAPIView is a view that allows us to create an object in the database
# The CreateAPIView is a generic view that comes with rest_framework


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    # The serializer_class is the serializer that we want to use to create the object
    serializer_class = UserSerializer


# ObtainAuthToken is a view that comes with rest_framework that handles creating authentication tokens
# ObtainAuthToken is a generic view that comes with rest_framework

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    # The serializer_class is the serializer that we want to use to create the object
    # AuthTokenSerializer is a serializer that we created in the user app
    serializer_class = AuthTokenSerializer
    # The renderer_classes are the renderer classes that we want to use to render the view
    # Is not active by default, we need to add it
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# RetrieveUpdateAPIView is a view that allows us to retrieve and update an object from the database
# Retrieving: HTTP GET request
# Updating: HTTP PATCH request or HTTP PUT request

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    # The authentication_classes are the authentication classes that we want to use to authenticate the user
    authentication_classes = [authentication.TokenAuthentication]
    # The permission_classes are the permission classes that we want to use to authenticate the user
    permission_classes = [permissions.IsAuthenticated]

    # The get_object is a function that is called when we make a HTTP GET request to the view
    # The get_object is a function that is called to retrieve the model object
    # The get_object is a function that is called to retrieve the model object that we want to return in the response
    def get_object(self):
        """Retrieve and return authenticated user"""
        # self.request.user is the user that is authenticated
        # self.request.user is the user that is authenticated by the authentication_classes
        # self.request.user is the user that is authenticated by the authentication_classes that we added to the view
        return self.request.user
