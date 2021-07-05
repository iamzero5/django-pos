from products.models import Product
from sales.models import Document
from members.models import Member,CommonFields
from django.db import models
from django.urls import reverse

class AccountsPayable(Document):
    member = models.ForeignKey(Member,null=True,on_delete=models.SET_NULL,default=None)
    products = models.ManyToManyField(Product, through="AccountsPayableProduct")
    def __str__(self):
        return f"AP{self.pk:07}"

    def get_absolute_url(self):
        return reverse("accountspayable_api", kwargs={"pk": self.pk})

class AccountsPayableProduct(CommonFields):
    account_payable = models.ForeignKey(AccountsPayable,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12,decimal_places=2)
    price = models.DecimalField(max_digits=12,decimal_places=2)
    amount = models.DecimalField(max_digits=12,decimal_places=2)

    class Meta:
        unique_together = ['account_payable','product']