from django.urls import path
from .views import add_to_cart_view


app_name = "product"
urlpatterns = [
    path('add_to_cart/',add_to_cart_view, name='add-to-cart-url'),

]