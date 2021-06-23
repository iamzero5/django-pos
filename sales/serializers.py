from products.models import Product
from rest_framework import serializers
from .models import SalesOrder,SalesOrderProduct
from products.serializers import ProductSerializers
import datetime

class SalesOrderProductSerializers(serializers.ModelSerializer):
    product_id = serializers.ReadOnlyField(source="product.id")
    product_name = serializers.ReadOnlyField(source="product.name")
    class Meta:
        model = SalesOrderProduct
        fields = ['id','product_id','product_name','quantity','price','amount']

class SalesOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = SalesOrder
        fields = ['id','posting_date','document_status','remarks','member',
        'reference_number','products','total_amount','paid_amount','payment_type','url']

    url = serializers.URLField(source='get_absolute_url', read_only=True)
    products = SalesOrderProductSerializers(source="salesorderproduct_set",many=True)

    def create(self,validated_data):
        user = self.context.get('user')
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        products_data = self.context.get('products')
        price_data = self.context.get('price')
        quantity_data = self.context.get('quantity')
        so = SalesOrder.objects.create(**validated_data)
        so.total_amount = 0.0
        so.document_status = "C"
        for i in range(0,len(products_data)):
            prod = Product.objects.get(pk=int(products_data[i]))
            sop = SalesOrderProduct.objects.create(sales_order=so,product=prod,quantity=quantity_data[i],price=price_data[i],amount=float(price_data[i])*float(quantity_data[i]))
            sop.updated_by = user
            sop.created_by = user
            so.total_amount += sop.amount
            sop.save()
        return so

    def update(self,instance,validated_data):
        user = self.context.get('user')
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.is_standard = validated_data.get('is_standard',instance.is_standard)
        instance.price = validated_data.get('price',instance.price)
        instance.updated_by = user
        instance.save()
        return instance