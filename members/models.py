import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class CommonFields(models.Model):
    created_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="%(class)s_created_by")
    updated_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name="%(class)s_updated_by")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def updatedby(self,user):
        updated_by = user

    class Meta:
        abstract = True

class Company(CommonFields):
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=150)
    barangay = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100,blank=True)
    mobile = models.CharField(max_length=100)
    email = models.EmailField(max_length=150,null=True)

class Branch(CommonFields):
    company = models.ForeignKey(Company,on_delete=models.RESTRICT)
    name = models.CharField(max_length=120)
    street = models.CharField(max_length=150)
    barangay = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100,blank=True)
    mobile = models.CharField(max_length=100)
    email = models.EmailField(max_length=150,null=True)

class Membership(CommonFields):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_standard = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=12,decimal_places=2,help_text="Price per month.")

    def get_absolute_url(self):
        return reverse("membership_api", kwargs={"pk": self.pk})
    

class Bank(CommonFields):
    name = models.CharField(max_length=100)

class Person(CommonFields):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100)

    class Meta:
        abstract = True

class SalesPerson(Person):
    active = models.BooleanField(default=True)

class PersonalTrainer(Person):
    active = models.BooleanField(default=True)

class Member(Person):

    MEMBERSTATUSES = (
            ('N','None'),
            ('A','Active'),
            ('I','Inactive'),
            ('C','Cancelled')
        )

    GENDERS = (
        ('M','Male'),
        ('F','Female')
        )
    
    CARD_TYPES = (
        ('M','Mastercard'),
        ('V','Visa')
        )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    birthdate = models.DateField()
    gender = models.CharField(max_length=2,choices=GENDERS,default="M")
    street = models.CharField(max_length=150)
    barangay = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    telephone = models.CharField(max_length=100,blank=True)
    mobile = models.CharField(max_length=100)
    email = models.EmailField(max_length=150,null=True)

    membership = models.ForeignKey(Membership,on_delete=models.CASCADE,null=True)
    membership_start = models.DateField(null=True)
    membership_term = models.PositiveIntegerField(default=0)
    membership_status = models.CharField(max_length=2,choices=MEMBERSTATUSES,default='N')
    access_key = models.CharField(max_length=100,blank=True,unique=True)
    access_key_released = models.BooleanField(default=False)
    sales_person = models.ForeignKey(SalesPerson,null=True,on_delete=models.SET_NULL)
    personal_trainer = models.ForeignKey(PersonalTrainer,null=True,on_delete=models.SET_NULL)

    bank = models.ForeignKey(Bank,null=True,on_delete=models.SET_NULL)
    card_holder = models.CharField(max_length=100,null=True)
    card_number = models.CharField(max_length=100,null=True)
    card_expiry = models.DateField(null=True)
    card_type = models.CharField(max_length=2,choices=CARD_TYPES,blank=True)

    #user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="%(class)s_user",null=True)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse("member_api", kwargs={"pk": self.pk})

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class MemberMembershipLog(CommonFields):
    membership = models.ForeignKey(Membership,on_delete=models.CASCADE)
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    membership_start = models.DateField()
    membership_term = models.PositiveIntegerField()

    class Meta:
        unique_together = ('membership','member','membership_start')

class MemberAttendance(CommonFields):
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(null=True)