from rest_framework import serializers
from .models import Product,Package,PackageProduct
from django.contrib.auth.models import User

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name','product_type','price','url']

    url = serializers.URLField(source='get_absolute_url', read_only=True)

    def create(self,validated_data):
        user = self.context.get('user')
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        return Product.objects.create(**validated_data)

    def update(self,instance,validated_data):
        user = self.context.get('user')
        instance.name = validated_data.get('name',instance.name)
        instance.name = validated_data.get('image',instance.image)
        instance.name = validated_data.get('price',instance.price)
        instance.updated_by = user
        instance.save()
        return instance

class PackageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['name','price','url']

    url = serializers.URLField(source='get_absolute_url', read_only=True)

    def create(self,validated_data):
        user = self.context.get('user')
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        return Package.objects.create(**validated_data)

    def update(self,instance,validated_data):
        user = self.context.get('user')
        instance.name = validated_data.get('name',instance.name)
        instance.name = validated_data.get('price',instance.price)
        instance.updated_by = user
        instance.save()
        return instance