from .member import *
from .membership import *
from .salesperson import *
from .personaltrainer import *
import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from members.models import Member,Membership, SalesPerson,PersonalTrainer

@login_required
def index(request):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    week = datetime.date.today() + datetime.timedelta(days=7)
    new_members = Member.objects.filter(membership_start__gte=yesterday).count()
    renewals = Member.objects.filter(membership_end__lte=week).count()
    return render(request,'members/index.html',{"new_members":new_members,"renewals":renewals})