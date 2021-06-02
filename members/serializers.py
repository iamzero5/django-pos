from rest_framework import serializers
from .models import Member,Bank,Membership,SalesPerson,PersonalTrainer
from products.models import Product
from django.contrib.auth.models import User
import datetime

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
        fields = ['id','first_name','middle_name','last_name','birthdate','street','barangay','city','province','telephone','mobile','email','membership','membership_start','membership_term','sales_person','personal_trainer','url','membership_status_display']
    
    membership_status_display = serializers.CharField(source='get_membership_status_display',read_only=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    def create(self,validated_data):
        validated_data['created_by'] = self.context['user']
        validated_data['updated_by'] = self.context['user']
        v_start = datetime.strptime(validated_data['membership_start'],'%Y-%m-%d')
        validated_data['membership_end'] = v_start + datetime.timedelta(days=validated_data['membership_term'])
        return Member.objects.create(**validated_data)

class SalesPersonSerializers(serializers.ModelSerializer):
    class Meta:
        model = SalesPerson
        fields = ['id','first_name','middle_name','last_name','active','url']

    url = serializers.URLField(source='get_absolute_url', read_only=True)

    def create(self,validated_data):
        user = self.context.get('user')
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        return SalesPerson.objects.create(**validated_data)

    def update(self,instance,validated_data):
        user = self.context.get('user')
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.middle_name = validated_data.get('middle_name',instance.middle_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.active = validated_data.get('active',instance.active)
        instance.updated_by = user
        instance.save()
        return instance

class PersonalTrainerSerializers(serializers.ModelSerializer):
    class Meta:
        model = PersonalTrainer
        fields = ['id','first_name','middle_name','last_name','active','url']

    url = serializers.URLField(source='get_absolute_url', read_only=True)

    def create(self,validated_data):
        user = self.context.get('user')
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        return PersonalTrainer.objects.create(**validated_data)

    def update(self,instance,validated_data):
        user = self.context.get('user')
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.middle_name = validated_data.get('middle_name',instance.middle_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.active = validated_data.get('active',instance.active)
        instance.updated_by = user
        instance.save()
        return instance