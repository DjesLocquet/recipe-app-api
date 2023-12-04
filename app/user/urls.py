"""
Urls mappings for the user API.
"""

from django.urls import path

from user import views

# The app_name is the name of the app that we want to use to identify the urls
# We can use this app_name to reverse look up the urls in our tests
# The app_name is used in the reverse function, e.g. reverse('user:create')

app_name = 'user'

urlpatterns = [
    # The name is the name that we are going to use to identify the url
    # The name is used in the reverse function, e.g. reverse('user:create')
    # The second argument is the view that we want to use for this url, and must be a function
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
