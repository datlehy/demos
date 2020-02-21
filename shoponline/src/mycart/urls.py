'''
Created on Nov 12, 2017

@author: lhdat
'''
from mycart import views
from django.conf.urls import url

app_name = 'mycart'

urlpatterns = [
    url(r'^cart_add/(\d+)/$', views.cart_add, name='cart_add'),
    url(r'^cart_remove/(\d+)/$', views.cart_remove, name='cart_remove'),
    url(r'^cart_detail/$', views.cart_detail, name='cart_detail'),
]
