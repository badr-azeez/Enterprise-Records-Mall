from django.db import models
from administrator.models import Departments
from django.contrib.auth.models import User
import uuid ,os
from datetime import datetime

year = datetime.today().year
month = datetime.today().month
day = datetime.today().day

def save_record_file(instance, filename):
    uuid_token = uuid.uuid4().hex
    first_department = uuid_token.split('-')[0][0:5]
    extension = os.path.splitext(filename)[1]
    new_filename = f"{first_department}{extension}"
    old_name = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    new_filename = f"{instance.user.first_name}_{old_name}_{first_department}{extension}"
    return f'files_records/{year}/{month}/{day}/id_{instance.user.id}/{new_filename}'

def save_uploadFile(instance, filename):
    # Generate a UUID token and take the first department
    uuid_token = uuid.uuid4().hex
    first_department = uuid_token.split('-')[0][0:5]
    # Extract file extension and create a new filename
    old_name = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    new_filename = f"{instance.user.first_name}_{old_name}_{first_department}{extension}"

    return f'files/{year}/{month}/{day}/id_{instance.user.id}/{new_filename}'


class Records(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="user")
    department = models.ForeignKey(Departments, on_delete=models.CASCADE,verbose_name="department")
    note = models.TextField(verbose_name="note",null=True,blank=True,default="")
    date = models.DateField(verbose_name="date",help_text="date.png")
    date_creation = models.DateTimeField(auto_now_add=True,verbose_name="added at")
    last_modified = models.DateTimeField(auto_now=True,verbose_name="modified at")
    file = models.FileField(upload_to=save_record_file,verbose_name="file",blank=True,null=True)
    is_validate = models.BooleanField(verbose_name='validate?',default=False)
    field_1 = models.PositiveIntegerField(verbose_name="Bath & Body products", default=0, help_text='bath.png')
    field_2 = models.PositiveIntegerField(verbose_name="Beauty and cosmetics products", default=0, help_text='beauty.png')
    field_3 = models.PositiveIntegerField(verbose_name="Books and stationery", default=0, help_text='books.png')
    field_4 = models.PositiveIntegerField(verbose_name="Electronics", default=0, help_text='electronics.png')
    field_5 = models.PositiveIntegerField(verbose_name="Kitchen gadgets and cookware", default=0, help_text='kitchen.png')
    field_6 = models.PositiveIntegerField(verbose_name="Musical instruments and accessories", default=0, help_text='musical.png')
    field_7 = models.PositiveIntegerField(verbose_name="Pet supplies and accessories", default=0, help_text='pet-shop.png')
    field_8 = models.PositiveIntegerField(verbose_name="Sports Goods & Equipment", default=0, help_text='sports.png')
    field_9 = models.PositiveIntegerField(verbose_name="Tools and hardware", default=0, help_text='tools.png')
    field_10 = models.PositiveIntegerField(verbose_name="Toys and games", default=0, help_text='toys.png')
    field_11 = models.PositiveIntegerField(verbose_name="Video Games and Consoles", default=0, help_text='video-games.png')


class uploadFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Account Owner")
    department = models.ForeignKey(Departments, on_delete=models.CASCADE,verbose_name="Department")
    title = models.CharField(verbose_name="subject",max_length=255,default='')
    note = models.TextField(verbose_name="note",null=True,blank=True,default="")
    date = models.DateField(verbose_name="upload date")
    date_creation = models.DateTimeField(auto_now_add=True,verbose_name="added at")
    last_modified = models.DateTimeField(auto_now=True,verbose_name="modified at")
    file = models.FileField(upload_to=save_uploadFile,verbose_name="file",blank=True,null=True)
    is_validate = models.BooleanField(verbose_name='validated?',default=False)
