from django.db import models
from django.conf import settings

# Create your models here.

class Topping(models.Model):
    name = models.CharField(max_length=100)
    # topping price depends on size
    price_small = models.DecimalField(max_digits=5, decimal_places=2)
    price_medium = models.DecimalField(max_digits=5, decimal_places=2)
    price_large = models.DecimalField(max_digits=5, decimal_places=2)
    # is_vegan = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    PIZZA_SIZES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large')] # just for choices
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, help_text="Optional description for the pizza") 
    base_price_small = models.DecimalField(max_digits=5, decimal_places=2)
    base_price_medium = models.DecimalField(max_digits=5, decimal_places=2)
    base_price_large = models.DecimalField(max_digits=5, decimal_places=2)
    # any topping can be added to any pizza
    image = models.ImageField(upload_to='pizzas/', blank=True, null=True) # Optional
    # featured = models.BooleanField(default=False) 

    def __str__(self):
        return self.name

class Drink(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2) # simple price
    image = models.ImageField(upload_to='drinks/', blank=True, null=True) # Optional
    # stock_count = models.IntegerField(default=0) # stock tracking?

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    is_completed = models.BooleanField(default=False) # for order status
    # notes = models.TextField(blank=True) # special comments on order?

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.SET_NULL, null=True, blank=True)
    drink = models.ForeignKey(Drink, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    # For Pizzas:
    size = models.CharField(max_length=1, choices=Pizza.PIZZA_SIZES, null=True, blank=True)
    selected_toppings = models.ManyToManyField(Topping, blank=True) # toppings for specific pizza in the order
    price_at_purchase = models.DecimalField(max_digits=6, decimal_places=2) # price of the item when ordered
    # special_instructions = models.CharField(max_length=255, blank=True) # for this item?

    def __str__(self):
        if self.pizza:
            return f"{self.quantity}x {self.pizza.name} ({self.get_size_display()})"
        return f"{self.quantity}x {self.drink.name}"

    def get_item_total(self):
        return self.quantity * self.price_at_purchase



