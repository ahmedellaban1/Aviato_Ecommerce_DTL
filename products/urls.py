from django.urls import path
from .views import home_page_view, shop_products_view, product_details_view, categories_view

app_name = "product"
urlpatterns = [
    path('',home_page_view, name='home-page-url'),
    path('shop', shop_products_view, name='shop-products-url'),
    path('shop/product-<int:pk>/', product_details_view, name='product-details-url'),
    path('shop/categories/', categories_view, name='all-categories-url'),

]