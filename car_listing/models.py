from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField()
    price = models.CharField(max_length=100)
    price_currency = models.CharField(max_length=20)
    mileage = models.CharField(max_length=100)
    fuel_type = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    gearbox = models.CharField(max_length=50, blank=True, null=True)
    horsepower = models.CharField(max_length=50, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField()
    engine_capacity = models.CharField(max_length=50, default='Unknown')

    def __str__(self):
        return self.name
