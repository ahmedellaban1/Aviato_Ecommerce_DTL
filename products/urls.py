from django.urls import path
from .views import home_page_view, shop_products_view

app_name = "product"
urlpatterns = [
    path('',home_page_view, name='home-page-url'),
    path('shop/', shop_products_view, name='shop-products-url')
]