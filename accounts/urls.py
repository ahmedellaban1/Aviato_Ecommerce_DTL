from django.urls import path
from .views import create_user_view


app_name = "accounts"
urlpatterns = [
    path('sign-up/', create_user_view, name='create-user-url'),
]
