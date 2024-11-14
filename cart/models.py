from django.db import models
from authentication.models import User
from boats.models import BoatInstance

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Cart for {self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    boat_instance = models.ForeignKey(BoatInstance, on_delete=models.CASCADE)
    number_of_days = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.number_of_days * self.price_per_day
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.boat_instance} in Cart {self.cart}"