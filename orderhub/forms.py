from django import forms
from .models import OrderItem

class AddToCard(forms.Form):
   product = forms.IntegerField()
   color = forms.IntegerField()
   size = forms.IntegerField()
   quantity = forms.IntegerField(min_value=1)
