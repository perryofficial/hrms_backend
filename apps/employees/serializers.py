from rest_framework import serializers

from .models import Department, Designation, Employee


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = [
            "id",
            "name",
        ]
        read_only_fields = [
            "id",
        ]


class DesignationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Designation
        fields = [
            "id",
            "name",
        ]
        read_only_fields = [
            "id",
        ]


class EmployeeWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = [
            "user",
            "employee_code",
            "first_name",
            "last_name",
            "date_of_joining",
            "department",
            "designation",
        ]


class EmployeeSerializer(serializers.ModelSerializer):

    department = DepartmentSerializer(read_only=True)
    designation = DesignationSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "user",
            "employee_code",
            "first_name",
            "last_name",
            "date_of_joining",
            "department",
            "designation",
        ]
        read_only_fields = [
            "id",
            "department",
            "designation",
        ]