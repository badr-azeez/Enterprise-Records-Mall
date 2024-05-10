# tables.py
import django_tables2 as tables
from django_tables2 import columns , Column
from .models import Records ,uploadFile
from django.contrib.auth.models import User
from django.utils.html import mark_safe


class ValidateColumn(Column):
    def render(self, record):
        if record.is_validate:
            return mark_safe(f'<div class="text-center"><i class="fa-solid fa-check fa-lg" style="color: #63E6BE;"></i></div>')
        else:
            return mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;"></i></div>')


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


class titleColumn(Column):
    def render(self, record):
        if len(record.title) >= 30:
            return record.title[0:30] + "..."
        else:
            return record.title

class recordsTableForUser(tables.Table):
    id = columns.Column(exclude_from_export=True)
    user = ownColumn()
    note = noteColumn(attrs={"td": {"style":"font-size:15px"}},default=mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;font-size:25px;padding-top:16px;"></i></div>') )
    file = fileColumn(default=mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;"></i></div>'))
    is_validate = ValidateColumn(default=mark_safe('<div class="text-center"><i class="fa-solid fa-xmark fa-lg" style="color:  #ea538f;"></i></div>'))
    last_modified = columns.DateTimeColumn(format="Y-m-d  h:i A",exclude_from_export=True)
    date = columns.DateTimeColumn(format="Y-m-d",exclude_from_export=True,verbose_name="Date")

    action = columns.TemplateColumn(
        template_name="users/tmps/records_action.html",
        orderable=False,exclude_from_export=True,
            verbose_name="Actions",attrs={
                "a": {"class": "btn btn-success fa fa-pen"},
                "td": {"class":"text-center"},
                "th": {"class":"text-center"}
            }
    )
    class Meta:
        model = Records
        exclude = ("id",'date_creation','department','field_1','field_2','field_3','field_4','field_5','field_6','field_7','field_8','field_9','field_10','field_11','field_12','field_13', 'field_14','field_15','field_16','field_17','field_18','field_19','field_20','field_21','field_22','field_23')
        sequence = ['user','date','is_validate','last_modified','note','file','action']


class uploadFileTableForUser(tables.Table):
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
        template_name="users/tmps/upload_file_action.html",
        orderable=False,exclude_from_export=True,
            verbose_name="Actions",attrs={
                "a": {"class": "btn btn-success fa fa-pen"},
                "td": {"class":"text-center"},
                "th": {"class":"text-center"}
            }
    )
    class Meta:
        model = uploadFile
        exclude = ("id",'date_creation','department','last_modified')
        sequence = ['user','date','is_validate','title','note','file','action']
