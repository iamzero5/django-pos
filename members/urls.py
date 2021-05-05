from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.index,name="index"),
    path('memberships/',views.MembershipListView.as_view(),name="memberships"),
    path('membership',views.MembershipList.as_view(),name="membership"),
    path('membership/api/<int:pk>',views.MembershipDetail.as_view(),name="membership_api"),
    path('members/',views.MemberListView.as_view(),name="members"),
    path('member',views.MemberList.as_view(),name="member"),
    path('member/api/<int:pk>',views.MemberDetail.as_view(),name="member_api")
]