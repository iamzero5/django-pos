from .member import *
from .membership import *
from .salesperson import *
from .personaltrainer import *
from .bank import *
import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from members.models import Member
from sales.models import SalesOrder
from django.db.models import Sum

@login_required
def index(request):
    yesterday = datetime.date.today() - datetime.timedelta(days=7)
    week = datetime.date.today() + datetime.timedelta(days=7)
    new_members = Member.objects.filter(membership_start__gte=yesterday).count()
    members = Member.objects.all().order_by('-membership_start')[:8]
    month = datetime.date.today().month
    sales = SalesOrder.objects.filter(posting_date__month=month).aggregate(grand_total=Sum("total_amount"))
    renewals = Member.objects.filter(membership_end__lte=week).count()
    return render(request,'members/index.html',{"members":members,"new_members":new_members,"renewals":renewals,"sales":sales})