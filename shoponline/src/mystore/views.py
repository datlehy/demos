from django.shortcuts import render

# Create your views here.
from mystore.models import Product, OrderItem
from _datetime import datetime
from django.http.response import HttpResponse
from mycart import forms
from mystore.forms import  UserForm, UserProfileInfoForm, OrderCreateForm

from mycart.cart import Cart
import profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    date1 = datetime.now()
    value = request.COOKIES.get('last_visit', \
                                date1.strftime('%d-%m-%Y %H:%M:%S'))
    pro_list = Product.objects.order_by('name')
    pro_dict = {'products' : pro_list, 'last_visit' : value}
    response = render(request, "mystore/index.html", context=pro_dict)
    response.set_cookie('last_visit', \
                        date1.strftime('%d-%m-%Y %H:%M:%S'))
    return response


def product_detail(request, id=None):
    product = Product.objects.get(pk=id)
    cart_product_form = forms.CardAddProductForm()
    return render(request, 'mystore/product_detail.html', \
                  context={'product':product, \
                             'cart_product_form':cart_product_form})


def read_cookie(request):
    value = request.COOKIES.get('last_visit')
    text = "<h3>The last time to visit this page is %s</h3>" % value
    return HttpResponse(text)


def register(request):
    registered = False
    if request.method == 'POST':
        form_user = UserForm(data=request.POST)
        form_por = UserProfileInfoForm(data=request.POST)
        if form_user.is_valid() and form_por.is_valid():
            user = form_user.save(commit=False)
            user.set_password(user.password)
            user.save()
            
            profile = form_por.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            
            registered = True
            
        else:
            print(form_user.error, form_por.error)
    else:
        form_user = UserForm()
        form_por = UserProfileInfoForm()
        
    return render(request, 'mystore/registration.html', \
                  context={'user_form': form_user, \
                             'profile_form': form_por, \
                             'registered': registered})


def user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        passwd = request.POST.get('password')
        user = authenticate(username=uname, password=passwd)
        if user:
            if user.is_active:
                login(request, user)
                # clean cart
                cart = Cart(request)
                cart.clear()
                
                result = 'Welcome ' + uname
                cart = Cart(request)
                cart.user = uname
                return render(request, 'mystore/index.html', \
                              context={'result': result})
        else:
            print('login failed')
            login_result = 'username and password is invalid'
            return render(request, 'mystore/login.html', \
                          context={'login_result': login_result})
    else:
        return render(request, 'mystore/login.html')

    
@login_required
def user_logout(request):
    logout(request)
    # clean cart
    cart = Cart(request)
    cart.clear()
    
    result = 'You already log out . You should log in'
    return render(request, 'mystore/index.html', \
                  context={'result': result})


def order_create(request):
    cart = Cart(request)
    form = OrderCreateForm()
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, \
                                         product=item['product'], \
                                         price=item['fee'], \
                                         quantity=item['quantity'])
            
            cart.clear()
            return render(request, 'mystore/created.html', \
                          context={'order': order})
    else:
        form = OrderCreateForm()
        return render(request, 'mystore/create.html', \
                      context={'form': form})
