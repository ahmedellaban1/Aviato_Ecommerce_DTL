from django.urls import path
from .views import create_user_view, verify_mail_view


app_name = "accounts"
urlpatterns = [
    path('sign-up/', create_user_view, name='create-user-url'),
    path('sign-up/verify_mail/', verify_mail_view, name='verify-mail-url'),
]
