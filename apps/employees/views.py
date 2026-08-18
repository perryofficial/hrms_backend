from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Department, Designation, Employee
from .serializers import (
    DepartmentSerializer,
    DesignationSerializer,
    EmployeeSerializer,
    EmployeeWriteSerializer,
)
# Create your views here.
class DepartmentListCreateView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request):

        departments = Department.objects.all()

        serializer = DepartmentSerializer(
            departments,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):

        serializer = DepartmentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        department = serializer.save()

        return Response(
            DepartmentSerializer(department).data,
            status=status.HTTP_201_CREATED,
        )



class DesignationListCreateView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request):

        designations = Designation.objects.all()

        serializer = DesignationSerializer(
            designations,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):

        serializer = DesignationSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        designation = serializer.save()

        return Response(
            DesignationSerializer(designation).data,
            status=status.HTTP_201_CREATED,
        )



class EmployeeListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        employees = Employee.objects.select_related(
            "user",
            "department",
            "designation",
        )

        serializer = EmployeeSerializer(
            employees,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def post(self, request):

        serializer = EmployeeWriteSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        employee = serializer.save()

        return Response(
            EmployeeSerializer(employee).data,
            status=status.HTTP_201_CREATED,
        )




class EmployeeDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, id):

        return Employee.objects.select_related(
            "user",
            "department",
            "designation",
        ).get(id=id)

    def get(self, request, id):

        employee = self.get_object(id)

        serializer = EmployeeSerializer(employee)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


    
    def put(self, request, id):

        employee = self.get_object(id)

        serializer = EmployeeWriteSerializer(
            employee,
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True
        )

        employee = serializer.save()

        return Response(
            EmployeeSerializer(employee).data,
            status=status.HTTP_200_OK,
        )


    def patch(self, request, id):

        employee = self.get_object(id)

        serializer = EmployeeWriteSerializer(
            employee,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True
        )

        employee = serializer.save()

        return Response(
            EmployeeSerializer(employee).data,
            status=status.HTTP_200_OK,
        )


    def delete(self, request, id):

        employee = self.get_object(id)

        employee.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )