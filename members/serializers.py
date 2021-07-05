from rest_framework import serializers
from .models import Member,Membership,SalesPerson,PersonalTrainer,Bank,MembershipTerm
import datetime

class MembershipTermSerializers(serializers.ModelSerializer):
    class Meta:
        model = MembershipTerm
        fields = ['month','valid_from','valid_to','url']

    url = serializers.URLField(source="get_absolute_url",read_only=True)

    def create(self,validated_data):
        user = self.context.get('user')
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        return MembershipTerm.objects.create(**validated_data)

    def update(self,instance,validated_data):
        user = self.context.get('user')
        instance.month = validated_data.get('days',instance.month)
        instance.valid_from = validated_data.get('valid_from',instance.valid_from)
        instance.valid_to = validated_data.get('valid_to',instance.valid_to)
        instance.updated_by = user
        instance.save()
        return instance
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
        fields = ['id','first_name','middle_name','last_name','gender','birthdate','street','barangay','city','province',
        'telephone','mobile','email','membership','membership_start','membership_term','membership_status','sales_person',
        'personal_trainer','access_key','access_key_released','bank','card_type','card_holder','card_number','card_expiry',
        'url','membership_status_display']
    
    membership_status_display = serializers.CharField(source='get_membership_status_display',read_only=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    def create(self,validated_data):
        validated_data['created_by'] = self.context['user']
        validated_data['updated_by'] = self.context['user']
        validated_data['membership_status'] = 'A' if validated_data['membership'] != None else 'N'
        validated_data['access_key_released'] = True if validated_data['access_key_released'] != None else False
        validated_data['membership_end'] = validated_data.get('membership_start') + datetime.timedelta(days=int(validated_data.get('membership_term').month)*30)
        if validated_data['membership_end'] < datetime.date.today() and validated_data['membership_status'] !='F':
            validated_data['membership_status'] = 'I'
        return Member.objects.create(**validated_data)

    def update(self,instance,validated_data):
        user = self.context.get('user')
        instance.first_name = validated_data.get('first_name',instance.first_name)
        instance.middle_name = validated_data.get('middle_name',instance.middle_name)
        instance.last_name = validated_data.get('last_name',instance.last_name)
        instance.gender = validated_data.get('gender',instance.gender)
        instance.birthdate = validated_data.get('birthdate',instance.birthdate)
        instance.street = validated_data.get('street',instance.street)
        instance.barangay = validated_data.get('barangay',instance.barangay)
        instance.city = validated_data.get('city',instance.city)
        instance.province = validated_data.get('province',instance.province)
        instance.telephone = validated_data.get('telephone',instance.telephone)
        instance.mobile = validated_data.get('mobile',instance.mobile)
        instance.email = validated_data.get('email',instance.email)
        instance.membership = validated_data.get('membership',instance.membership)
        instance.membership_start = validated_data.get('membership_start',instance.membership_start)
        instance.membership_term = validated_data.get('membership_term',instance.membership_term)
        instance.sales_person = validated_data.get('sales_person',instance.sales_person)
        instance.personal_trainer = validated_data.get('personal_trainer',instance.personal_trainer)
        instance.bank = validated_data.get('bank',instance.bank)
        instance.card_type = validated_data.get('card_type',instance.card_type)
        instance.card_holder = validated_data.get('card_holder',instance.card_holder)
        instance.card_number = validated_data.get('card_number',instance.card_number)
        instance.card_expiry = validated_data.get('card_expiry',instance.card_expiry)
        instance.membership_status = 'A' if instance.membership != None else 'N'
        instance.access_key = validated_data.get('access_key',instance.access_key)
        instance.access_key_released = True if validated_data.get('access_key_released') != None else False
        instance.membership_end = instance.membership_start + datetime.timedelta(days=int(instance.membership_term.month)*30)
        today = datetime.date.today()
        if instance.membership_end < today and instance.membership_status != 'F':
            instance.membership_status = 'I'
        instance.updated_by = user
        instance.save()
        return instance

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

class BankSerializers(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id','name','url']

    url = serializers.URLField(source='get_absolute_url', read_only=True)

    def create(self,validated_data):
        user = self.context.get('user')
        validated_data['created_by'] = user
        validated_data['updated_by'] = user
        return Bank.objects.create(**validated_data)

    def update(self,instance,validated_data):
        user = self.context.get('user')
        instance.name = validated_data.get('name',instance.name)
        instance.updated_by = user
        instance.save()
        return instance