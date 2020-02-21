'''
Created on Nov 19, 2017

@author: hv
'''
from mycart.cart import Cart


def cart(request):
    return {'cart': Cart(request)}
