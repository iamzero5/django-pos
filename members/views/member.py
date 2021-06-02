import datetime
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from members.models import Member,Membership, SalesPerson,PersonalTrainer
from members.serializers import MemberSerializers

#MemberModule
class MemberListView(PermissionRequiredMixin,LoginRequiredMixin,ListView):
    permission_required = ('is_staff','members.view_member')
    model = Member
    template_name = "members/member.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gender_choices'] = Member.GENDERS
        context['memberships'] = Membership.objects.all()
        context['salespersons'] = SalesPerson.objects.filter(active=True)
        context['personaltrainers'] = PersonalTrainer.objects.filter(active=True)
        return context

class MemberList(APIView):
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        snippets = Member.objects.all()
        serializer = MemberSerializers(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MemberSerializers(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemberDetail(APIView):
    #permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self,pk):
        try:
            return Member.objects.get(pk=pk)
        except Member.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        instance = self.get_object(pk)

        if not instance:
            return Response(
                {"res":"Member does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = MemberSerializers(instance)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )

    def put(self,request,pk):
        instance = self.get_object(pk)

        if not instance:
            return Response(
                {"res":"Member does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MemberSerializers(instance = instance,data=request.data,context={'user':request.user},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,pk):
        instance = self.get_object(pk)

        if not instance:
            return Response(
                {"res":"Member does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.delete()
        return Response(
            {"res":"Member has been deleted!"},
            status = status.HTTP_200_OK
        )