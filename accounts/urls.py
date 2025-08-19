from django.urls import path
from .views import create_user_view, verify_mail_view, log_out_view, profile_details_view, update_profile_view


app_name = "accounts"
urlpatterns = [
    path('log-out/', log_out_view, name='log-out-url'),
    path('sign-up/', create_user_view, name='create-user-url'),
    path('sign-up/verify_mail/', verify_mail_view, name='verify-mail-url'),
    path('my-profile/', profile_details_view, name='profile-details-url'),
    path('my-profile/update/', update_profile_view, name='update-profile-url')
]
