from django.db import models
from authentication.models import User
from boats.models import BoatInstance

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status= models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

class OrderBoat(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_boats')
    boat = models.ForeignKey(BoatInstance, on_delete=models.CASCADE)
    days = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Boat {self.boat} in Order {self.order}"

class Pago(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_address = models.CharField(max_length=255)
    method = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.method} - {self.account_number}"