from django.urls import path
from . import views

app_name="administrator"

urlpatterns = [
    path('departments',views.departmentsList,name="departments"),
    path('departments/add',views.addDepartment,name="departments/add"),
    path('departments/edit/<pk>',views.editDepartment,name="departments_edit"),
    path('departments/delete/<pk>',views.deleteDepartment,name="departments/delete"),
    path('users',views.usersList,name="users"),
    path('users/add',views.addUser,name="users/add"),
    path('user/edit/<pk>',views.editUser,name="user-edit"),
    path('users/delete/<pk>',views.deleteUser,name="users-delete"),
    path('records-departments',views.recordsDepartmentsList,name='records/departments'),
    path('file-uploaded',views.fileUploadedList,name='file-uploaded'),
    path('records-extract',views.recordsExtract,name='records/extracts'),
]
