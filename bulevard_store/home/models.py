from django.conf import settings
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/category/%Y/%m/%d/')

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    count = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_images(self):
        return Image.objects.filter(item_id=self)

    def get_image(self):
        return Image.objects.filter(item_id=self)[0]


class Image(models.Model):
    image = models.ImageField(upload_to='images/item/%Y/%m/%d/')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    apartment = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)

    ordered = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.IntegerField()
