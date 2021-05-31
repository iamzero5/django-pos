from rest_framework import serializers
from .models import Member,Bank,Membership
from products.models import Product
from django.contrib.auth.models import User

class MembershipSerializers(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id','name','description','is_standard','price','url']

    url = serializers.URLField(source='get_absolute_url', read_only=True)

    def create(self,validated_data):
        user = self.context.get('user')
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        return Membership.objects.create(**validated_data)

    def update(self,instance,validated_data):
        user = self.context.get('user')
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description',instance.description)
        instance.is_standard = validated_data.get('is_standard',instance.is_standard)
        instance.price = validated_data.get('price',instance.price)
        instance.updated_by = user
        instance.save()
        return instance

class MemberSerializers(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id','first_name','middle_name','last_name','birthdate','street','barangay','city','province','telephone','mobile','email','url','membership_status_display']
    
    membership_status_display = serializers.CharField(source='get_membership_status_display',read_only=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    def create(self,validated_data):
        validated_data['created_by'] = self.context['user']
        validated_data['updated_by'] = self.context['user']
        return Member.objects.create(**validated_data)