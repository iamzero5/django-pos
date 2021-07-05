import datetime
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import SalesOrder,SalesOrderProduct
from ..serializers import SalesOrderSerializers,SalesOrderProductSerializers
from members.models import Member
from products.models import Product

#SalesOrderModule
class SalesOrderListView(PermissionRequiredMixin,LoginRequiredMixin,ListView):
    permission_required = ('is_staff','sales.view_salesorder')
    model = SalesOrder
    template_name = "sales/salesorder.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['members'] = Member.objects.all()
        context['products'] = Product.objects.all()
        context['payment_types'] = SalesOrder.PAYMENT_TYPES
        context['document_statuses'] = SalesOrder.DOCUMENT_STATUSES
        return context

class SalesOrderList(APIView):
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        snippets = SalesOrder.objects.all()
        serializer = SalesOrderSerializers(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SalesOrderSerializers(data=request.data,context={'user':request.user,'products':request.data.getlist('products'),'quantity':request.data.getlist('quantity'),'price':request.data.getlist('price')})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SalesOrderDetail(APIView):
    #permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self,pk):
        try:
            return SalesOrder.objects.get(pk=pk)
        except SalesOrder.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        instance = self.get_object(pk)

        if not instance:
            return Response(
                {"res":"Sales Order does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SalesOrderSerializers(instance)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )

    def put(self,request,pk):
        instance = self.get_object(pk)

        if not instance:
            return Response(
                {"res":"Sales Order does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SalesOrderSerializers(instance = instance,data=request.data,context={'user':request.user},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,pk):
        instance = self.get_object(pk)

        if not instance:
            return Response(
                {"res":"Sales Order does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.delete()
        return Response(
            {"res":"Sales Order has been deleted!"},
            status = status.HTTP_200_OK
        )