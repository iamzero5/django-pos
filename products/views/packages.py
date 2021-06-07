from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Package
from ..serializers import PackageSerializers

#MembershipModule
class PackageListView(PermissionRequiredMixin,LoginRequiredMixin,ListView):
    permission_required = ('is_staff','Packages.view_Package')
    model = Package
    template_name = "packages/package.html"

class PackageList(APIView):
    #permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        snippets = Package.objects.all()
        serializer = PackageSerializers(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PackageSerializers(data=request.data,context={'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PackageDetail(APIView):
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    
    def get_object(self,pk):
        try:
            return Package.objects.get(pk=pk)
        except Package.DoesNotExist:
            raise Http404

    def get(self,request,pk,format=None):
        instance = self.get_object(pk)

        if not instance:
            return Response(
                {"res":"Package does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = PackageSerializers(instance)
        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )

    def put(self,request,pk):
        instance = self.get_object(pk)

        if not instance:
            return Response(
                {"res":"Package does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PackageSerializers(instance = instance,data=request.data,context={'user':request.user},partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self,request,pk):
        instance = self.get_object(pk)

        if not instance:
            return Response(
                {"res":"Package does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.delete()
        return Response(
            {"res":"Package has been deleted!"},
            status = status.HTTP_200_OK
        )