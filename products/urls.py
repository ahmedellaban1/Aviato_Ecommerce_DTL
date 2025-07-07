from django.urls import path, include
from .views import home_page_view

app_name = "product"
urlpatterns = [
    path('',home_page_view, name='home-page'),
]