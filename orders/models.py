from django.db import models
from authentication.models import User
from boats.models import BoatInstance

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status= models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

class OrderBoat(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_boats')
    boat = models.ForeignKey(BoatInstance, on_delete=models.CASCADE)
    days = models.IntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Boat {self.boat} in Order {self.order}"

class Pago(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('on_site', 'Pagar en sitio'),
        ('online', 'Pagar en línea'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_address = models.CharField(max_length=255, null=True, blank=True)
    method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    account_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.method} - {self.account_number}"
    
class Cliente(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    telephone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    dni = models.CharField(max_length=10)
    birthdate = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.surname}"