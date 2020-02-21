'''
Created on Nov 18, 2017

@author: hv
'''
from django import forms
from django.contrib.auth.models import User
from mystore.models import UserProfileInfo, Order


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta():
        model = User
        fields = ('username', 'email', 'password')

        
class UserProfileInfoForm(forms.ModelForm):
    # porfolio = forms.URLField(required = False)
    picture = forms.ImageField(required=False)
    
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio', 'picture')

        
class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['firstName', 'lastName', 'email', 'address']

        
def clear(self):
    self.cart = {}
    self.save()
