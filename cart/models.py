from django.db import models
from authentication.models import User
from boats.models import BoatInstance

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user}"
        return f"Cart for session {self.session_key}"
    
    def get_total_price(self):
        fee = 0
        price_without_fee = sum(item.total_price for item in self.items.all())
        if price_without_fee > 0:
            fee = 30
        if price_without_fee > 1000:
            fee = 0
        return price_without_fee + fee

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    boat_instance = models.ForeignKey(BoatInstance, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_days = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.number_of_days * self.boat_instance.model.price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.boat_instance} in Cart {self.cart}"