"""
Serializers for user API view.
"""

from django.contrib.auth import (
                                get_user_model,
                                authenticate,
                                )

from django.utils.translation import ugettext_lazy as _     # Default syntax for translating strings into different languages in Django
from rest_framework import serializers

# Serializers are used to convert data inputs into Python objects and vice versa
# The serializer takes a json input, it validates it, and then converts it into a Python object or a model from the database
# There are different types of BaseClass serializers, ModelSerializer is a serializer that is specifically for Django models
# ModelSerializer can validate the input on the fields that are required, and it also has a create function that allows us to create a new object in the database

# The serializer is used in the view, the view is the API endpoint that we are going to create


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    # Meta class is a configuration for the serializer
    # The model is the model that we want to base the serializer on
    # The fields are the fields that we want to include in the serializer
    # The extra_kwargs are the extra keyword arguments that we can pass to the fields
    # The extra_kwargs are used to configure some extra settings in our model fields
    # The extra_kwargs are used to make the password field write only, so that it can only be used to create or update an object, but not to retrieve an object
    # The extra_kwargs are used to set the minimum length of the password field to 5 characters

    class Meta:
        """Meta class for the serializer"""
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        # The create is called after the validation is passed
        # The validated_data is the validated data that is passed to the serializer
        # The validated_data is a dictionary of all the fields that were passed to the serializer
        # The validated_data is passed as a keyword argument to the create_user function

        # The default create function for the ModelSerializer is to create and return the model object
        # We are overriding the default create function to create and return the user object with the encrypted password
        # The create_user function is a custom function that we created in the user manager

        return get_user_model().objects.create_user(**validated_data)

    # Instance is the model instance that gone be updated
    # The validated_data is the validated data that has passed the validation
    def update(self, instance, validated_data):
        """Update and return the user, setting the password correctly"""
        password = validated_data.pop('password', None)    # pop = get and remove the password from the validated_data
        user = super().update(instance, validated_data)    # The super function is a Python function that calls the update function on the ModelSerializer BaseClass

        if password:
            user.set_password(password)
            user.save()

        # Return the user object as expected by the view that is calling the serializer
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    # The serializer is used to authenticate the user
    # The serializer is used to validate the authentication request

    # The email and password fields are the fields that we want to use to authenticate the user
    # The email and password fields are the fields that we want to validate
    # The email and password fields are required fields
    # The email and password fields are used to authenticate the user
    # The email and password fields are used to validate the authentication request

    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},   # The style is used to configure the HTML input type, so that the password is not visible when typing it
        trim_whitespace=False       # DRF by default will trim the whitespace at the end of the password, we don't want that, so we set it to False
    )

    # The validate function is a function that is called when we validate the serializer
    # The validate function is used to validate the data that is passed to the serializer
    # The validate function is used to validate the authentication request
    # attrs is a short for attributes

    def validate(self, attrs):
        """Validate and authenticate the user"""
        # The attrs is a dictionary of all the fields that are passed to the serializer
        # The attrs is a dictionary of all the fields that are validated by the serializer

        # The authenticate function is a Django helper function that is used to authenticate the user
        # The authenticate function is used to authenticate the user with the email and password
        # The authenticate function is used to authenticate the user with the email and password that are passed to the serializer

        email = attrs.get('email')
        password = attrs.get('password')

        # The authenticate function is a Django helper function that is used to authenticate the user
        # The authenticate function is used to authenticate the user with the email and password
        # The authenticate function is used to authenticate the user with the email and password that are passed to the serializer

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        # If the authentication fails, raise an exception
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        # The attrs is a dictionary of all the fields that are passed to the serializer
        # The attrs is a dictionary of all the fields that are validated by the serializer

        # The user is the user object that is authenticated
        # The user is the user object that is authenticated with the email and password that are passed to the serializer
        # This is what the view expects to receive

        attrs['user'] = user
        return attrs
