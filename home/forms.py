from django import forms
from django.contrib.auth.models import User

# just show fields to template
class LoginUser(forms.ModelForm):
    username  = forms.CharField(label="Username",min_length=3,max_length=50,help_text="Must be between 3 to 50 English characters")
    password  = forms.CharField(label="Password",min_length=8,max_length=100,help_text="It should be between 8 to 100 characters")
    class Meta:
        model = User
        fields = ['username','password']