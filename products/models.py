from django.db import models
from members.models import CommonFields,Branch
from django.urls import reverse
# Create your models here.
class Product(CommonFields):

    PRODUCTTYPES = (
        ('I','Item'),
        ('S','Service')
        )
    name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=2,choices=PRODUCTTYPES,default='I')
    image = models.ImageField(upload_to="products")
    price = models.DecimalField(max_digits=16,decimal_places=4)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product", kwargs={"pk": self.pk})
    
class ProductDiscount(CommonFields):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=5,decimal_places=2)
    is_active = models.BooleanField(default=True)

class Package(CommonFields):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=16,decimal_places=4)
    product = models.ManyToManyField(Product, through="PackageProduct")

class PackageProduct(CommonFields):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    package = models.ForeignKey(Package,on_delete=models.CASCADE)
    