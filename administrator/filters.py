import django_filters
from .models import Departments
from users.models import Records ,uploadFile
from django import forms
from django.contrib.auth.models import User

try:
    users_list = []
    for user in User.objects.exclude(id=1).all():
        users_list.append((user.id,user.first_name))
except:
    pass
class recordsFilter(django_filters.FilterSet):
    note = django_filters.CharFilter(label='Notes',field_name='note',lookup_expr='icontains') 
    date = django_filters.CharFilter(label='Date',field_name='date', widget=forms.TextInput(
        attrs={
            "class": "form-control bg-dark text-white custom-height",
            "id": "dateInput",
            "type" : "date"
        }
    ))
    
    is_validate = django_filters.ChoiceFilter(label='Validate?',field_name='is_validate',choices=((True,'Yes'),(False,'No')), widget=forms.Select(
        attrs={
            "class": "fs-5 form-select bg-info text-black",
            "max_length": "100"
        }
    ))
    department = django_filters.ModelChoiceFilter(label="Department", field_name='department', queryset = Departments.objects.exclude(id=1).all() ,widget=forms.Select(
        attrs={
            "class": "fs-5 form-select bg-info text-black",
            "max_length": "100"
        }
    ))
    user = django_filters.ChoiceFilter(label="Account Owner", field_name='user', choices=users_list ,widget=forms.Select(
        attrs={
            "class": "fs-5 form-select bg-info text-black",
            "max_length": "100"
        }
    ))
    class Meta:
        model = Records
        fields = ['note','date',"is_validate",'department','user'] 

class fileUploadedFilter(django_filters.FilterSet):
    note = django_filters.CharFilter(label='Note',field_name='Note',lookup_expr='icontains') 
    date = django_filters.CharFilter(label='Date',field_name='Date', widget=forms.TextInput(
        attrs={
            "class": "form-control bg-dark text-white custom-height",
            "id": "dateInput",
            "type" : "date"
        }
    ))
    
    is_validate = django_filters.ChoiceFilter(label='Validate?',field_name='is_validate',choices=((True,'Yes'),(False,'No')), widget=forms.Select(
        attrs={
            "class": "fs-5 form-select bg-info text-black",
            "max_length": "100"
        }
    ))
    department = django_filters.ModelChoiceFilter(label="Department", field_name='department', queryset = Departments.objects.exclude(id=1).all() ,widget=forms.Select(
        attrs={
            "class": "fs-5 form-select bg-info text-black",
            "max_length": "100"
        }
    ))
    user = django_filters.ChoiceFilter(label="Account Owner", field_name='user', choices=users_list ,widget=forms.Select(
        attrs={
            "class": "fs-5 form-select bg-info text-black",
            "max_length": "100"
        }
    ))
    class Meta:
        model = uploadFile
        fields = ['note','date',"is_validate",'department','user'] 

class UsersFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(label='Account Owner',field_name='first_name',lookup_expr='icontains',widget=forms.TextInput(
        attrs={
            "class": "form-control bg-dark text-white custom-height",
            "type" : "text"
        }
    )) 
    is_superuser = django_filters.ChoiceFilter(label='Admin?',field_name='is_superuser',choices=((True,'Yes'),(False,'No')), widget=forms.Select(
        attrs={
            "class": "fs-5 form-select bg-info text-black",
            "max_length": "100"
        }
    ))
    is_active = django_filters.ChoiceFilter(label='Active?',field_name='is_active',choices=((True,'Yes'),(False,'No')), widget=forms.Select(
        attrs={
            "class": "fs-5 form-select bg-info text-black",
            "max_length": "100"
        }
    ))
    class Meta:
        model = User
        fields = ['first_name','is_superuser','is_active'] 
