"""
Database models.
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin,
                                        )


class UserManager(BaseUserManager):
    """Manager for user profiles"""

    # **extra_fields keyword argument accepts any number of keyword arguments key=value
    def create_user(self, email, password=None, **extra_fields):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        # Set password as encrypted, hash the password
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create a new superuser profile"""
        # **extra_fields keyword argument accepts any number of keyword arguments key=value
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""

    # Email is the username and should be unique
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    # This user can access the admin page
    is_staff = models.BooleanField(default=False)

    # Defines the fields that are used to log in, email is used as username
    USERNAME_FIELD = 'email'

    objects = UserManager()


# Simple Model Base Class from Django
class Recipe(models.Model):
    """Recipe object"""

    # ForeignKey allows us to create a relationship between two different models
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # Defined in settings.py, best practice to use this instead of the direct reference to the model, because it allows us to change the model in the future
        on_delete=models.CASCADE,   # If the user is deleted, then the recipe is also deleted
    )
    title = models.CharField(max_length=255)    # Designed to store short strings, used in most cases
    description = models.TextField(blank=True)  # Designed to store more content and multiple lines of text, not used everywhere because it's less performant (SQL)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        # Is used in the Django admin, otherwise there will be just an id in the admin
        return self.title
