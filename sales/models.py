from members.models import CommonFields
from django.db import models
from products.models import Product
from members.models import Member
from django.urls import reverse

class Document(CommonFields):
    DOCUMENT_STATUSES = (
        ('O','Open'),
        ('D','Draft'),
        ('C','Closed'),
        ('CN','Cancelled')
    )
    PAYMENT_TYPES = (
        ('C','Cash'),
        ('CC','Credit Card')
    )
    posting_date = models.DateField()
    document_status = models.CharField(max_length=2,choices=DOCUMENT_STATUSES,default="O")
    remarks = models.TextField(max_length=1000,null=True)
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    reference_number = models.CharField(max_length=100,null=True)
    total_amount = models.DecimalField(max_digits=12,decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12,decimal_places=2)
    payment_type = models.CharField(max_length=2,choices=PAYMENT_TYPES,default='C')
    
    class Meta:
        abstract = True

class SalesOrder(Document):
    products = models.ManyToManyField(Product, through="SalesOrderProduct")
    def __str__(self):
        return f"SO{self.pk:07}"

    def get_absolute_url(self):
        return reverse("salesorder_api", kwargs={"pk": self.pk})


class SalesOrderProduct(CommonFields):
    sales_order = models.ForeignKey(SalesOrder,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12,decimal_places=2)
    price = models.DecimalField(max_digits=12,decimal_places=2)
    amount = models.DecimalField(max_digits=12,decimal_places=2)

    class Meta:
        unique_together = ['sales_order','product']

class AccountReceivable(Document):
    products = models.ManyToManyField(Product, through="AccountReceivableProduct")
    def __str__(self):
        return f"AR{self.pk:07}"

    def get_absolute_url(self):
        return reverse("accountreceivable_api", kwargs={"pk": self.pk})
    

class AccountReceivableProduct(CommonFields):
    account_receivable = models.ForeignKey(AccountReceivable,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12,decimal_places=2)
    price = models.DecimalField(max_digits=12,decimal_places=2)
    amount = models.DecimalField(max_digits=12,decimal_places=2)

    class Meta:
        unique_together = ['account_receivable','product']