from django import forms
from django.contrib.auth.models import User
from .models import Records,uploadFile
from django.template.defaultfilters import filesizeformat
from django.conf import settings
import re

# check file upload size less than 20.0 MB
class BaseFileUploadForm(forms.ModelForm):
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError('Please upload a file less than %s. File uploaded %s' % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE),
                    filesizeformat(file.size)
                ))
        return file
    
class CreateUploadFile(BaseFileUploadForm):

    class Meta:
        model = uploadFile
        exclude = ['user','department']

# create edit records
class CreateRecords(BaseFileUploadForm):
    class Meta:
        model = Records
        exclude = ['user','department']