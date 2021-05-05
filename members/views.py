import datetime
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from rest_framework import status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Member,Membership
from .serializers import MemberSerializers, MembershipSerializers

@login_required
def index(request):
    return render(request,'members/index.html')

#MembershipModule
class MembershipListView(LoginRequiredMixin,ListView):
    model = Membership
    template_name = "members/membership.html"

class MembershipList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        snippets = Membership.objects.all()
        serializer = MembershipSerializers(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MembershipSerializers(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MembershipDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self,pk):
        try:
            return Membership.objects.get(pk=pk)
        except Membership.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        instance = self.get_object(pk)

        if not instance:
            return Response(
                {"res":"Membership does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = MembershipSerializers(instance)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )

    def put(self,request,pk):
        instance = self.get_object(pk)

        if not instance:
            return Response(
                {"res":"Membership does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MembershipSerializers(instance = instance,data=request.data,context={'user':request.user},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,pk):
        instance = self.get_object(pk)

        if not instance:
            return Response(
                {"res":"Membership does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.delete()
        return Response(
            {"res":"Membership has been deleted!"},
            status = status.HTTP_200_OK
        )

#MemberModule
class MemberListView(LoginRequiredMixin,ListView):
    model = Member
    template_name = "members/member.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gender_choices'] = Member.GENDERS
        return context

class MemberList(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]
    
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