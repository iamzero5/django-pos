from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('dashboard/',views.index,name="index"),
    path('memberships/',views.MembershipListView.as_view(),name="memberships"),
    path('membership',views.MembershipList.as_view(),name="membership"),
    path('membership/api/<int:pk>',views.MembershipDetail.as_view(),name="membership_api"),
    path('members/',views.MemberListView.as_view(),name="members"),
    path('member',views.MemberList.as_view(),name="member"),
    path('member/<int:pk>',views.MemberDetailView.as_view(),name="member-detail"),
    path('member/freeze/<int:member_id>',views.member_freeze,name="member-freeze"),
    path('member/cancel/<int:member_id>',views.member_cancel,name="member-cancel"),
    path('member/api/<int:pk>',views.MemberDetail.as_view(),name="member_api"),
    path('member/upload/photo/<int:member_id>',views.member_photo_upload,name="member-upload-photo"),
    path('membershipterms/',views.MembershipTermListView.as_view(),name="membershipterms"),
    path('membershipterm',views.MembershipTermList.as_view(),name="membershipterm"),
    path('membershipterm/api/<int:pk>',views.MembershipTermDetail.as_view(),name="membershipterm_api"),
    path('salesperson/',views.SalesPersonListView.as_view(),name="salespersons"),
    path('salesperson',views.SalesPersonList.as_view(),name="salesperson"),
    path('salesperson/api/<int:pk>',views.SalesPersonDetail.as_view(),name="salesperson_api"),
    path('bank/',views.BankListView.as_view(),name="banks"),
    path('bank',views.BankList.as_view(),name="bank"),
    path('bank/api/<int:pk>',views.BankDetail.as_view(),name="bank_api"),
    path('personaltrainer/',views.PersonalTrainerListView.as_view(),name="personaltrainers"),
    path('personaltrainer',views.PersonalTrainerList.as_view(),name="personaltrainer"),
    path('personaltrainer/api/<int:pk>',views.PersonalTrainerDetail.as_view(),name="personaltrainer_api"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)