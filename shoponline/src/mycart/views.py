from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from mystore.models import Product
from .forms import CardAddProductForm

# Create your views here.


@require_POST
def cart_add(request, product_id=None):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CardAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
        print(cart)
        return redirect('mycart:cart_detail')


def cart_remove(request, product_id=None):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('mycart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CardAddProductForm(initial={'quantity': item['quantity'], 'update': True})
        
    return render(request, 'mycart/cart_detail.html', context={'cart':cart})
    
