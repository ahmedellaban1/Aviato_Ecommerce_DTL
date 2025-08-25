from django.urls import path
from .views import add_to_cart_view, products_cart_view, all_invoice_view, invoice_details_view


app_name = "orderhub"
urlpatterns = [
    path('add_to_cart/', add_to_cart_view, name='add-to-cart-url'),
    path('cart/', products_cart_view, name='products-cart-url'),
    path('orders/', all_invoice_view, name='all-inovices-url'),
    path('orders-details/', invoice_details_view, name='inovice-details-url'),
]
