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

class Membership(CommonFields):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_standard = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=12,decimal_places=2,help_text="Price per month.")

    def get_absolute_url(self):
        return reverse("membership_api", kwargs={"pk": self.pk})
    

class Bank(CommonFields):
    name = models.CharField(max_length=100)

class Member(CommonFields):

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100,blank=True)
    last_name = models.CharField(max_length=100)
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
    membership_end = models.DateField(null=True)
    membership_status = models.CharField(max_length=2,choices=MEMBERSTATUSES,default='N')
    access_key = models.CharField(max_length=100,blank=True,unique=True)
    staff_assigned = models.ForeignKey(User,null=True,on_delete=models.SET_NULL,related_name="%(class)s_staff")

    bank = models.ForeignKey(Bank,null=True,on_delete=models.SET_NULL)
    card_holder = models.CharField(max_length=100,null=True)
    card_number = models.CharField(max_length=100,null=True)
    card_expiry = models.DateField(null=True)

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="%(class)s_user",null=True)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        return reverse("member_api", kwargs={"pk": self.pk})

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class MemberAttendance(CommonFields):
    member = models.ForeignKey(Member,on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(null=True)