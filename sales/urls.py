from django.urls import path
from . import views

urlpatterns = [
    path('salesorders/',views.SalesOrderListView.as_view(),name="salesorders"),
    path('salesorder',views.SalesOrderList.as_view(),name="salesorder"),
    path('salesorder/api/<int:pk>',views.SalesOrderDetail.as_view(),name="salesorder_api"),
]