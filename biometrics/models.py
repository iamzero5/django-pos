from django.db import models
from members.models import CommonFields

class Biometric(CommonFields):
    ip = models.IPAddressField()
    port = models.IntegerField()
    commkey = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100,unique=True)
    mac = models.CharField(max_length=30,unique=True)
    active = models.BooleanField(default=True)