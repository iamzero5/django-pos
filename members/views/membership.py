from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from members.models import Membership
from members.serializers import MembershipSerializers
#MembershipModule
class MembershipListView(PermissionRequiredMixin,LoginRequiredMixin,ListView):
    permission_required = ('is_staff','members.view_membership')
    model = Membership
    template_name = "members/membership.html"

class MembershipList(APIView):
    #permission_classes = [permissions.IsAuthenticated]

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
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    
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
