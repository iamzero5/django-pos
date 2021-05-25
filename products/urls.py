from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.ProductListView.as_view(),name="products"),
    path('product',views.ProductList.as_view(),name="product"),
    path('product/api/<int:pk>',views.ProductDetail.as_view(),name="product_api"),
]