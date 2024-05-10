from django import forms
from django.contrib.auth.models import User
from .models import  Departments
import re

class CreateDepartments(forms.ModelForm):
    name = forms.CharField(label="Department Name",help_text="Field is required",required=True,error_messages={"invalid": "Field is required"})

    class Meta:
        model = Departments
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data['name']
        if Departments.objects.filter(name=name).exists():
            raise forms.ValidationError(f"The department already exists: {name}")
        return name
    
class CreateUser(forms.ModelForm):
    first_name  = forms.CharField(label="Name Account Owner",min_length=3,max_length=50,help_text="Must be between 3 to 50 English characters")
    username  = forms.CharField(label="Username",min_length=3,max_length=50,help_text="Must be between 3 to 50 English characters")
    password  = forms.CharField(label="Password",min_length=8,max_length=100,help_text="It should be between 8 to 100 characters")
    department = forms.ModelChoiceField(label="Department",queryset=Departments.objects.all(),required=True,widget=forms.Select(attrs={"class": "form-select"}),help_text="Field is required")
    class Meta:
        model = User
        fields = ['first_name','username','password','department']

    def clean_username(self):
        username = self.cleaned_data['username']
        
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"The user already exists: {username}")
        
        # lower english from 3 to 50
        pattern = r'^[a-z0-9_]{3,50}$'
        if not re.match(pattern, username):
            raise forms.ValidationError(f"Username format is incorrect Accepted characters must be (lowercase English letter, numbers, _) : {username}")
        
        return username