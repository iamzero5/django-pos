from rest_framework import serializers
from .models import Member,Bank,Membership
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
        instance.name = validated_data.get('description',instance.description)
        instance.name = validated_data.get('is_standard',instance.is_standard)
        instance.name = validated_data.get('price',instance.price)
        instance.updated_by = user
        instance.save()
        return instance

class MemberSerializers(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id','first_name','middle_name','last_name','birthdate','street','barangay','city','province','telephone','mobile','email']

    def create(self,validated_data):
        user = User.objects.create_user(validated_data.get('email'),validated_data.get('email'),'User12354')
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.save()
        validated_data['user'] = user
        validated_data['created_by'] = self.context['request'].user
        validated_data['updated_by'] = self.context['request'].user
        return Member.objects.create(**validated_data)