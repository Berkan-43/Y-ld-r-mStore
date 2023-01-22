from django import forms
from order.models import *

class ShopCartForm(forms.ModelForm): 
    class Meta:
        model = ShopCart
        fields = ['quantity']

class FavoriesForm(forms.ModelForm): 
    class Meta:
        model = ShopCart
        fields = ['quantity']

# class OrderForm(forms.ModelForm): 
#     class Meta:
#         model = Order
#         fields = [
#             'first_name',
#             'last_name',
#             'address',
#             'phone',
#             'city',
#             'country'
#         ]