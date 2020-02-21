from django.conf import settings
from mystore.models import Product

# Create your models here.


class Cart(object):
    
    def __init__(self, request):
        '''
        initialize the session
        '''
        
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
            
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
        
    def add(self, product, quantity=1, update_quantity=False):
        '''
        add product to cart or update its quanity
        '''
        product_id = str(product.pk)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity' : 0, 'fee' : product.fee}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
                
        self.save()
        
    def remove(self, product):
        product_id = str(product.pk)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
            
    def clear(self):
        self.cart = {}
        self.save()
            
    def __iter__(self):
        '''
        iterate over items in cart and get product from database
        
        '''
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        for product in products:
            self.cart[str(product.pk)]['product'] = product
            
        for item in self.cart.values():
            item['fee'] = item['fee']
            item['total_fee'] = float(item['fee']) * item['quantity']
            yield item
                
    def __len__(self):
        '''
        count all item in cart
        '''
        return sum(int(item['quantity']) for item in self.cart.values())
    
    def get_total_fee(self):
        '''
        get total fee products
        '''
        return sum(float(item['fee']) * int(item['quantity']) for item in self.cart.values())
