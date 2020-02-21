from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=264, unique=True)
    fee = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to="images/")
    
    def __str__(self):
        return str(self.name)
    

class UserProfileInfo(models.Model):
    # create relationship from this class to User
    user = models.OneToOneField(User, on_delete=False)
    # add any more attribute you want
    portfolio = models.URLField(blank=True)
    picture = models.ImageField(upload_to="images/", blank=True)
    
    def __str__(self):
        return self.user.username

    
class Order(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-created',)   
        
    def __str__(self):
        return 'Order{}'.format(self.id)
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=False, related_name='items')
    product = models.ForeignKey(Product, on_delete=False, related_name='item')
    price = models.FloatField()
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
    
