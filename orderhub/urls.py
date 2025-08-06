from django.urls import path
from .views import add_to_card_view


app_name = "product"
urlpatterns = [
    path('add_to_card/',add_to_card_view, name='add-to-card-url'),

]