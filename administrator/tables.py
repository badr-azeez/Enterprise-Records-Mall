# tables.py
import django_tables2 as tables
from django_tables2 import columns , Column
from .models import Departments  , userDepartment
from users.models import Records , uploadFile
from django.contrib.auth.models import User
from django.utils.html import mark_safe


class SuperuserIconColumn(Column):
    def render(self, record):
        is_superuser = record.is_superuser
        if is_superuser:
            return mark_safe('<div class="text-center"><i class="fa-solid fa-check fa-lg" style="color: #63E6BE;"></i></div>')
        else:
            return mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;"></i></div>')


class ActiveIconColumn(Column):
    def render(self, record):
        is_superuser = record.is_active
        if is_superuser:
            return mark_safe('<div class="text-center"><i class="fa-solid fa-check fa-lg" style="color: #63E6BE;"></i></div>')
        else:
            return mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;"></i></div>')

class departmentNameColumn(Column):
    def render(self, record):
        if record.username != 'admin':
            user_department = userDepartment.objects.get(user=record.id).department
            return user_department
        else:
            return mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;"></i></div>') 

class departmentLinkColumn(Column):
    def render(self, record):
        return mark_safe(f'<a class="link-info link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover" href="users?department={record.id}" >{record.name}</a>') 


class userDepartmentNumbersColumn(Column):
    def render(self, record):
        return userDepartment.objects.filter(department=record.id).count()



class noteColumn(Column):
    def render(self, record):
        if len(record.note) >= 30:
            return record.note[0:30] + "..."
        else:
            return record.note
class ownColumn(Column):
    def render(self, record):
        return record.user.first_name

class fileColumn(Column):
    def render(self, record):
        if record.file  and  len(record.file.url) > 0:
            return mark_safe(f'<div class="text-center"><a href="{record.file.url}" ><i class="fa-solid fa-download fa-sm fa-lg" style="color: #63E6BE;"></a></i></i></div>')
        else:
            return mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;"></i></div>')

class ValidateColumn(Column):
    def render(self, record):
        if record.is_validate:
            return mark_safe(f'<div class="text-center"><i class="fa-solid fa-check fa-lg" style="color: #63E6BE;"></i></div>')
        else:
            return mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;"></i></div>')





class usersTable(tables.Table):
    id = columns.Column(exclude_from_export=True)
    first_name = columns.Column(verbose_name='Account Owner',exclude_from_export=True)
    username = columns.Column(verbose_name='Username',exclude_from_export=True)
    is_superuser = SuperuserIconColumn(verbose_name='Account Admin?',exclude_from_export=True)
    is_active = ActiveIconColumn(verbose_name='Account Active?',exclude_from_export=True)
    last_login = columns.DateTimeColumn(format="Y-m-d  h:i A",verbose_name='Last login',exclude_from_export=True)
    ## i added is_staff because can't add new name  this field get data form departmentNameColumn
    is_staff = departmentNameColumn(verbose_name='Department Name')
    
    action = columns.TemplateColumn(
        template_name="administrator/tmps/user_action.html",
        orderable=False,
        exclude_from_export=True,
        verbose_name="Actions",
        attrs={
                "a": {"class": "btn btn-success fa fa-pen"},
                "td": {"class":"text-center"},
                "th": {"class":"text-center"}
            },
    )
    class Meta:
        model = User
        exclude = ("id","password","email","last_name",'date_joined')
        sequence = ('first_name', 'username','is_staff' ,'is_superuser','is_active','last_login', 'action')

class departmentsTable(tables.Table):
    id = columns.Column(exclude_from_export=True)
    id = userDepartmentNumbersColumn(verbose_name="count of Users")
    name = departmentLinkColumn(verbose_name="Department")
    action = columns.TemplateColumn(
        template_name="administrator/tmps/departments_action.html",
        orderable=False,exclude_from_export=True,
            verbose_name="Actions",attrs={
                "a": {"class": "btn btn-success fa fa-pen"},
                "td": {"class":"text-center"},
                "th": {"class":"text-center"}
            }
    )
    class Meta:
        model = Departments
        exclude = ('date_creation','last_modified' )
        sequence = ['name','id','action']

class recordsTableForAdmin(tables.Table):
    id = columns.Column(exclude_from_export=True)
    user = ownColumn()
    note = noteColumn(attrs={
                "td": {"style":"font-size:15px"},
            })
    file = fileColumn(default= mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;"></i></div>'))
    is_validate = ValidateColumn(default=mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;"></i></div>'))

    last_modified = columns.DateTimeColumn(format="Y-m-d  h:i A",exclude_from_export=True)
    date = columns.DateTimeColumn(format="Y-m-d",exclude_from_export=True)

    action = columns.TemplateColumn(
        template_name="administrator/tmps/records_action.html",
        orderable=False,exclude_from_export=True,
            verbose_name="Actions",attrs={
                "a": {"class": "btn btn-success fa fa-pen"},
                "td": {"class":"text-center"},
                "th": {"class":"text-center"}
            }
    )
    class Meta:
        model = Records
        exclude = ("id",'date_creation','field_1','field_2','field_3','field_4','field_5','field_6','field_7','field_8','field_9','field_10','field_11','field_12','field_13', 'field_14','field_15','field_16','field_17','field_18','field_19','field_20','field_21','field_22','field_23')
        sequence = ['department','user','date','is_validate','last_modified','note','file','action']
       

class recordsTableForAdminExport(tables.Table):
    user = ownColumn()

    date = columns.DateTimeColumn(format="Y-m-d")

    class Meta:
        model = Records
        exclude = ("id",'date_creation','file','last_modified','action','note')
        sequence = ['department','user','date']


class titleColumn(Column):
    def render(self, record):
        if len(record.title) >= 30:
            return record.title[0:30] + "..."
        else:
            return record.title

class uploadFileTableForAdmin(tables.Table):
    id = columns.Column(exclude_from_export=True)
    title = titleColumn()
    user = ownColumn()
    note = noteColumn(attrs={
                "td": {"style":"font-size:15px"},
            })
    file = fileColumn(default=mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;"></i></div>'))
    is_validate = ValidateColumn(default=mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;"></i></div>'))

    last_modified = columns.DateTimeColumn(format="Y-m-d  h:i A",exclude_from_export=True)
    date = columns.DateTimeColumn(format="Y-m-d",exclude_from_export=True)

    action = columns.TemplateColumn(
        template_name="administrator/tmps/upload_file_action.html",
        orderable=False,exclude_from_export=True,
            verbose_name="Actions",attrs={
                "a": {"class": "btn btn-success fa fa-pen"},
                "td": {"class":"text-center"},
                "th": {"class":"text-center"}
            }
    )
    class Meta:
        model = uploadFile
        exclude = ("id",'date_creation','last_modified')
        sequence = ['user','department','date','is_validate','title','note','file','action']

