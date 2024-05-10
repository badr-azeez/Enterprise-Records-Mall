from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from administrator.models import Departments ,  userDepartment
from users.models import Records , uploadFile
from .forms import LoginUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.db.models import Sum

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

def user_login(request): # this login for admin/user
    if request.user.is_authenticated:
        return redirect('home:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home:home')
        else:
            if User.objects.filter(username=username).exists():
                user =  User.objects.get(username=username)
                if user.is_active == False:
                    messages.error(request,"Your account is disabled")
                else:
                    messages.error(request,"Username or password is wrong")    
            else:
                messages.error(request,"Username or password is wrong")   

    context= {"form":LoginUser()}
    return render(request,'home/login.html',context)

@login_required(login_url='home:login')
def home(request): # this for  home user show  chars

    if request.user.is_superuser:  
        data = Records.objects.filter(is_validate=True).order_by('department')
        records_not_validate_yet =  Records.objects.filter(is_validate=False).order_by('department').count()
        departments = Departments.objects.exclude(id=1).all().order_by('name')
        
        ## get uploadFile this month
        uploadFile_dict = {}
        uploadFile_list = uploadFile.objects.filter(date__month=month)
        for department in departments:
            uploadFile_dict[department.name] = 'NotSet'

        for file_upload in uploadFile_list:
            if file_upload.is_validate:
                uploadFile_dict[file_upload.department.name] = 'True'
            else:
                uploadFile_dict[file_upload.department.name] = 'False'
        ##################################
        # get user login this day
        login_details = {}
        users = User.objects.filter(is_superuser=False).order_by('-last_login')
        for user in users:
            if user.last_login != None:
                if user.last_login.date() == today:
                    login_details[user] = 'Today'
                elif user.last_login.date() == yesterday:
                    login_details[user] = 'Yesterday'
                elif user.last_login.date() == last_2_day:
                    login_details[user] = 'since 2 day'
                elif user.last_login.date() == last_3_day:
                    login_details[user] = 'since 3 day'
                elif user.last_login.date() == last_4_day:
                    login_details[user] = 'since 4 day'
                elif user.last_login.date() == last_5_day:
                    login_details[user] = 'since 5 day'
                elif user.last_login.date() == last_6_day:
                    login_details[user] = 'since 6 day'
                elif user.last_login.date() >= week_ago:
                    login_details[user] = 'since week'
                else:
                    login_details[user] = user.last_login.strftime('%Y-%m-%d')
            else:
                login_details[user] = "User Not Login"        
        
        year_month_7days = {}
        total_departments_year_sum  = 0
        total_departments_month_sum = 0
        total_departments_7days_sum = 0
        for department in departments:
            department_7days_sum = 0
            department_month_sum = 0
            department_year_sum  = 0

            #get year
            for field_num in range(1, 11):
                field_name = f'field_{field_num}'
                # get total sum  or filed  
                field_sum = data.filter(department=department,date__year=year).aggregate(Sum(field_name))[f'{field_name}__sum']
                field_sum = field_sum or 0  #  field_sum  0 if None
                # add this field sum to variable
                department_year_sum += field_sum
            
            total_departments_year_sum += department_year_sum

            # add to dict
            year_month_7days[f'{department}'] = {"y":department_year_sum}

            #get month
            for field_num in range(1, 11):
                field_name = f'field_{field_num}'
                # get total sum  or filed  
                field_sum = data.filter(department=department,date__month=month).aggregate(Sum(field_name))[f'{field_name}__sum']
                #  field_sum  0 if None
                field_sum = field_sum or 0  
                # add this field sum to variable
                department_month_sum += field_sum

            total_departments_month_sum += department_month_sum
            # add to dict
            year_month_7days[f'{department}'].update({"m":department_month_sum})

            #get days_7
            for field_num in range(1, 11):
                field_name = f'field_{field_num}'
                # get total sum  or filed  
                field_sum = data.filter(department=department,date__month=month,date__day__gte=(day-7)).aggregate(Sum(field_name))[f'{field_name}__sum']
                #  field_sum  0 if None
                field_sum = field_sum or 0  
                department_7days_sum += field_sum

            total_departments_7days_sum += department_7days_sum
            # add to dict
            year_month_7days[f'{department}'].update({"days_7":department_7days_sum})

        context = { 'year_month_7days':year_month_7days,
                   'total_departments_7days_sum':total_departments_7days_sum ,
                   'total_departments_month_sum':total_departments_month_sum ,
                   'total_departments_year_sum':total_departments_year_sum ,
                   'uploadFile':uploadFile_dict,
                   'login_details':login_details,
                   'records_not_validate_yet':records_not_validate_yet,
                   'day':day,
                   'month':month,
                   'year':year,
                   }
        return render(request,'administrator/home.html',context)
    else:
        department_ins = userDepartment.objects.get(user=request.user)
        department = Departments.objects.get(pk=department_ins.department.id)
        data = Records.objects.filter(is_validate=True,department=department_ins.department).order_by('department')
        records_not_validate_yet =  Records.objects.filter(is_validate=False,department=department_ins.department).order_by('department').count()
        ## get file upload this month
        uploadFile_obj = uploadFile.objects.filter(date__month=month,department=department_ins.department).first()
        ##################################
        year_month_7days = {}
        total_departments_year_sum  = 0
        total_departments_month_sum = 0
        total_departments_7days_sum = 0
        department_7days_sum = 0
        department_month_sum = 0
        department_year_sum  = 0

        #get year
        for field_num in range(1, 11):
            field_name = f'field_{field_num}'
            # get total sum  or filed  
            field_sum = data.filter(department=department,date__year=year).aggregate(Sum(field_name))[f'{field_name}__sum']

            field_sum = field_sum or 0  #  field_sum  0 if None
            # add this field sum to variable
            department_year_sum += field_sum
        
        total_departments_year_sum += department_year_sum

        # add to dict
        year_month_7days[f'{department}'] = {"y":department_year_sum}

        #get month
        for field_num in range(1, 11):
            field_name = f'field_{field_num}'
            # get total sum  or filed  
            field_sum = data.filter(department=department,date__month=month).aggregate(Sum(field_name))[f'{field_name}__sum']
            #  field_sum  0 if None
            field_sum = field_sum or 0  
            # add this field sum to variable
            department_month_sum += field_sum

        total_departments_month_sum += department_month_sum
        # add to dict
        year_month_7days[f'{department}'].update({"m":department_month_sum})

        #get days_7
        for field_num in range(1, 11):
            field_name = f'field_{field_num}'
            # get total sum  or filed  
            field_sum = data.filter(department=department,date__month=month,date__day__gte=(day-7)).aggregate(Sum(field_name))[f'{field_name}__sum']
            #  field_sum  0 if None
            field_sum = field_sum or 0  
            department_7days_sum += field_sum

        total_departments_7days_sum += department_7days_sum
        # add to dict
        year_month_7days[f'{department}'].update({"days_7":department_7days_sum})

        context = { 'year_month_7days':year_month_7days,
                   'total_departments_7days_sum':total_departments_7days_sum ,
                   'total_departments_month_sum':total_departments_month_sum ,
                   'total_departments_year_sum':total_departments_year_sum ,
                   'uploadFile':uploadFile_obj,
                   'records_not_validate_yet':records_not_validate_yet,
                   'day':day,
                   'month':month,
                   'year':year,
                   'department':department_ins.department
                   }
        
        return render(request,'users/home.html',context)

@login_required(login_url='home:login')
def logout(request): 
    if request.method == 'POST':
        if request.user.is_authenticated:
            auth.logout(request)
    return redirect('home:login')

@login_required(login_url='login')
def about(request): 
    return render(request,'home/about.html')