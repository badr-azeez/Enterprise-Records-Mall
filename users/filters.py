import django_filters
from .models import Records , Departments,uploadFile
from django import forms
from django.contrib.auth.models import User


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