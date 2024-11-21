from django.db import models


class BoatType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class BoatModel(models.Model):
    boat_type = models.ForeignKey(BoatType, on_delete=models.SET_NULL, related_name='models', null=True)
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    brand = models.CharField(max_length=100)
    image = models.ImageField(upload_to='boat_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Port(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class BoatInstance(models.Model):
    model = models.ForeignKey(BoatModel, on_delete=models.SET_NULL, related_name='instances', null=True)
    name = models.CharField(max_length=100)
    port = models.ForeignKey(Port, on_delete=models.SET_NULL, related_name='instances', null=True)
    creation_date = models.DateField(auto_now_add=True)
    available = models.BooleanField(default=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
