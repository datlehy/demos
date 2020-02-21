'''
Created on Nov 12, 2017

@author: hv
'''
from django.conf.urls import url
from mystore import views

app_name = 'mystore'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^product_detail/(\d+)/$', views.product_detail, name='product_detail'),
    url(r'^readcookie/$', views.read_cookie, name='readcookie'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^create/', views.order_create, name='ordercreate'),
]
