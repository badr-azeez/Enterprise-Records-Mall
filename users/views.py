from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateRecords ,CreateUploadFile
from administrator.models import userDepartment
from .models import Records,uploadFile
from .tables import recordsTableForUser ,uploadFileTableForUser
import os
from datetime import datetime, timedelta
from django.utils import timezone

year = datetime.today().year
month = datetime.today().month
day = datetime.today().day
# Get today's date and calculate other date intervals
today = timezone.now().date()
yesterday = today - timedelta(days=1)
last_2_day = today - timedelta(days=2)
last_3_day = today - timedelta(days=3)
last_4_day = today - timedelta(days=4)
last_5_day = today - timedelta(days=5)
last_6_day = today - timedelta(days=6)
week_ago = today - timedelta(weeks=1)

#### records manager
@login_required(login_url='home:login')
def recordsList(request): # show records to users for each department
    if request.user.is_superuser:
       return redirect('home:home')
    
    sort  = request.GET.get('sort')
    if sort == None:
        sort = '-date_creation'
    # get user login department    
    user_info = userDepartment.objects.get(user=request.user.id)
    data = Records.objects.filter(department=user_info.department).order_by(sort)

    table = recordsTableForUser(data)
    table.paginate(page=request.GET.get("page", 1), per_page=15)

    context = {'table':table,'user_info':user_info}
    return render(request,'users/records.html',context=context)

@login_required(login_url='home:login')
def addRecord(request): # this for normal user to add record
   if request.user.is_superuser:
       return redirect('home:home')

   form = CreateRecords()
   # get user login department
   user_info = userDepartment.objects.get(user=request.user.id)
   if request.method == 'POST':
       form = CreateRecords(request.POST)
       if form.is_valid():
           form = CreateRecords(request.POST, request.FILES)
           form = form.save(commit=False)
           form.user = user_info.user
           form.department = user_info.department
           form.save()
           messages.success(request,'Record has been added')
           return redirect('users:records')
       
   context= {"form":form,
             'user_info':user_info
             }
   return render(request,'users/add_record.html',context)

@login_required(login_url='home:login')
def showRecord(request,pk): # show record for department users and admin
    record = Records.objects.get(pk=pk)
    department_name = record.department
    if not request.user.is_superuser:
        # get user login department
        user_info = userDepartment.objects.get(user=request.user.id)
        if user_info.department != department_name:
            return redirect('home:home')
    
    added_name = record.user
    last_modified = record.last_modified
    date_creation = record.date_creation
    record = CreateRecords(instance=record)

    context= {"record":record,
              'department_name':department_name,
              'added_name':added_name,
              'last_modified':last_modified,
              'date_creation':date_creation
              }

    return render(request,'users/show_record.html',context)

@login_required(login_url='home:login')
def editRecord(request,pk): # edit records to users for each department
    record = Records.objects.get(pk=pk)
    if (record.file):
        old_path = record.file.path
    else:
        old_path = ''
    department_name = record.department
    if not request.user.is_superuser:
        if request.user != record.user:
            return redirect('home:home')
        
        if record.is_validate == True:
            return redirect('home:home')
        request_data = request.POST.copy()
        if 'is_validate' in request_data:
            del request_data['is_validate']
        request.POST = request_data


    last_modified = record.last_modified
    date_creation = record.date_creation
    added_name = record.user
    form = CreateRecords(instance=record)
    
    if request.method == 'POST':
       form = CreateRecords(request.POST, request.FILES,instance=record)
       if form.is_valid():
           form = form.save(commit=False)
           form.user = added_name
           form.department = department_name
           if request.POST.get('checkFile') == 'deletefile':
               form.file = None
               if os.path.exists(old_path):
                  os.remove(old_path)
           
           if request.POST.get('checkFile') == 'uploadfile':
               if os.path.exists(old_path):
                  os.remove(old_path)

           form.save()
           messages.success(request,'Record Modified')
           if request.user.id != 1:
                return redirect('users:records')
           else:
                return redirect('administrator:records/departments')

    context= {"form":form,
              'department_name':department_name,
              'added_name':added_name,
              'last_modified':last_modified,
              'date_creation':date_creation
              }
    return render(request,'users/edit_record.html',context)

@login_required(login_url='home:login')
def deleteRecord(request,pk): # delete records to admin / users for each department
    record = Records.objects.get(pk=pk)
    if record.file:
        file = record.file.path
    else:
        file = ''
    if request.method == 'POST':
        if request.user.is_superuser:
            record.delete()
            if os.path.exists(file):
                os.remove(file)
            messages.success(request,'Record Deleted')
            return redirect('administrator:records/departments')
        else:
            # get user login department
            if request.user == record.user:
                if record.is_validate == True:
                    return redirect('home:home')
                record.delete()
                if os.path.exists(file):
                    os.remove(file)
                messages.success(request,'Record Deleted')

    return redirect('users:records')
#### end record manager

#### record file upload manager
@login_required(login_url='home:login')
def showUploadFile(request,pk):
    record = uploadFile.objects.get(pk=pk)
    last_modified = record.last_modified
    date_creation = record.date_creation
    department_name = record.department
    if not request.user.is_superuser:
        # get user login department
        user_info = userDepartment.objects.get(user=request.user.id)
        if user_info.department != department_name:
            return redirect('home:home')
        
    added_name = record.user
    form = CreateUploadFile(instance=record)
    context= {"form":form,
              'department_name':department_name,
              'added_name':added_name,
              'last_modified':last_modified,
              'date_creation':date_creation
              }
    return render(request,'users/show_upload_file.html',context)

@login_required(login_url='home:login')
def addUploadFile(request): # add/show file upload  only users
   if request.user.is_superuser:
       return redirect('home:home')
   
   form = CreateUploadFile()
   user_info = userDepartment.objects.get(user=request.user.id)

   sort  = request.GET.get('sort')
   if sort == None:
        sort = '-date'
   # get user login department
   user_info = userDepartment.objects.get(user=request.user.id)
   data = uploadFile.objects.filter(department=user_info.department).order_by(sort)
   table = uploadFileTableForUser(data)
   table.paginate(page=request.GET.get("page", 1), per_page=15)

   if request.method == 'POST':

       form = CreateUploadFile(request.POST,request.FILES)
       if form.is_valid():
           form = CreateUploadFile(request.POST, request.FILES)
           form = form.save(commit=False)
           form.user = user_info.user
           form.department = user_info.department
           form.save()
           messages.success(request,'File has been added')
           return redirect('users:upload-file')


   context= {"form":form,
             'user_info':user_info,
             'table':table,
             'user_info':user_info
             }
   return render(request,'users/upload_file.html',context)

@login_required(login_url='home:login')
def editUploadFile(request,pk): #edit file upload to admin / users for each department
    record = uploadFile.objects.get(pk=pk)
    if record.file:
        old_path = record.file.path
    else:
        old_path = ''
    department_name = record.department
    if not request.user.is_superuser:
        # get user login department
        user_info = userDepartment.objects.get(user=request.user.id)
        if request.user != record.user:
            return redirect('home:home')
        
        if record.is_validate == True:
            return redirect('home:home')
        
        request_data = request.POST.copy()
        if 'is_validate' in request_data:
            del request_data['is_validate']
        request.POST = request_data
        request.POST = request_data

    last_modified = record.last_modified
    date_creation = record.date_creation
    added_name = record.user
    form = CreateUploadFile(instance=record)
    
    if request.method == 'POST':

       form = CreateUploadFile(request.POST, request.FILES,instance=record)
       if form.is_valid():
           form = form.save(commit=False)
           form.user = added_name
           form.department = department_name
           if request.POST.get('checkFile') == 'deletefile':
               form.file = None
               if os.path.exists(old_path):
                  os.remove(old_path)
           
           if request.POST.get('checkFile') == 'uploadfile':
               if os.path.exists(old_path):
                  os.remove(old_path)

           form.save()
           messages.success(request,'Edit saved')

           if request.user.id != 1:
                return redirect('users:upload-file')
           else:
                return redirect('administrator:file-uploaded')

    context= {"form":form,
              'department_name':department_name,
              'added_name':added_name,
              'last_modified':last_modified,
              'date_creation':date_creation
              }
    return render(request,'users/edit_uploadFile.html',context)

@login_required(login_url='home:login')
def deleteUploadFile(request,pk): # delete file upload to admin / users for each department
    record = uploadFile.objects.get(pk=pk)
    if record.file:
        file = record.file.path
    else:
        file = ''
    if request.method == 'POST':
        if request.user.is_superuser:
            record.delete()
            if os.path.exists(file):
                os.remove(file)
            messages.success(request,'File Deleted')
            return redirect('users:upload-file')
        else:
            if request.user == record.user:

                if record.is_validate == True:
                    return redirect('home:home')
                record.delete()
                if os.path.exists(file):
                    os.remove(file)
                messages.success(request,'File deleted')

    return redirect('users:upload-file')
#### end file upload


################################## end normal user ##################################