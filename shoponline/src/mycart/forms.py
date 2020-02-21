'''
Created on Nov 12, 2017

@author: lhdat
'''
from django import forms
from builtins import int

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 10)]


class CardAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label='quantity', choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, widget=forms.HiddenInput)
