from django.db import models
from members.models import CommonFields,Membership
from django.urls import reverse
from django.db.models.signals import post_save
# Create your models here.
class Product(CommonFields):

    PRODUCTTYPES = (
        ('I','Item'),
        ('S','Service')
        )

    name = models.CharField(max_length=100)
    product_type = models.CharField(max_length=2,choices=PRODUCTTYPES,default='I')
    price = models.DecimalField(max_digits=12,decimal_places=2)
    membership = models.ForeignKey(Membership,on_delete=models.SET_NULL,null=True)
    sales = models.BooleanField(default=False)
    purchase = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_api", kwargs={"pk": self.pk})

def create_product(instance):
    product = Product()
    product.name = instance.name + " Membership"
    product.price = instance.price
    product.product_type = 'S'
    product.membership = instance
    product.created_by = instance.created_by
    product.updated_by = instance.updated_by
    product.save()

def create_product_for_membership(sender,instance,**kwargs):
    create_product(instance)

post_save.connect(create_product_for_membership,sender=Membership)
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
    