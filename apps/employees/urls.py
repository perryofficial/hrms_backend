from django.urls import path

from .views import (
    DepartmentListCreateView,
    DesignationListCreateView,
    EmployeeListCreateView,
    EmployeeDetailView,
)


urlpatterns = [
    path(
        "departments/",
        DepartmentListCreateView.as_view(),
        name="department-list-create",
    ),
    path(
        "designations/",
        DesignationListCreateView.as_view(),
        name="designation-list-create",
    ),
    path(
        "",
        EmployeeListCreateView.as_view(),
        name="employee-list-create",
    ),
    path(
        "<int:id>",
        EmployeeDetailView.as_view(),
        name="employee-detail",
    ),
]