"""
Database models.
"""

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
