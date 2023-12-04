"""
Django admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Translating text, _ is the alias for gettext function in Django translation module
# _ This alias is the standard convention in Django
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""

    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # The comma at the end is required to tell Python that it's a tuple
        # If you don't put the comma, Python will think it's just a string
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),)

    readonly_fields = ['last_login']

    # The add_fieldsets attribute overrides the base fieldsets attribute to add the email and password fields
    # The add_fieldsets attribute is used when creating new users
    # The add_fieldsets attribute is a tuple of tuples, it should be possible to also use a list of lists instead of a tuple of tuples
    # The class is to change the CSS style of the form, so that it's not too wide and it's easier to read, info from Django documentation
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'is_active', 'is_staff', 'is_superuser', )}),)


admin.site.register(models.User, UserAdmin)     # Uses a custom UserAdmin class
admin.site.register(models.Recipe)              # Uses the default Django Model so no need to pass a class
