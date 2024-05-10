from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateDepartments ,CreateUser
from .models import Departments,userDepartment
from users.models import Records , uploadFile
from .tables import departmentsTable ,usersTable ,recordsTableForAdmin,recordsTableForAdminExport, uploadFileTableForAdmin
from django_tables2.export.export import TableExport
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Sum
import io
from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Sum
from django.apps import apps
from .filters import recordsFilter ,fileUploadedFilter,UsersFilter

#### departments manager
@login_required(login_url='home:login')

def departmentsList(request): # show departments list
    if not request.user.is_superuser:
       return redirect('home:home')
    
    sort  = request.GET.get('sort')
    if sort == None:
        sort = '-date_creation'
    table = departmentsTable(Departments.objects.exclude(pk=1).all().order_by(sort))
    table.paginate(page=request.GET.get("page", 1), per_page=15)

    context = {'table':table}
    return render(request,'administrator/departments.html',context=context)

@login_required(login_url='home:login')

def addDepartment(request): # add department
    if not request.user.is_superuser:
       return redirect('home:home')
    
    form = CreateDepartments()
    if request.method == 'POST':
        form = CreateDepartments(request.POST)
        if form.is_valid():
            messages.success(request,"Department has been added")
            form.save()
            return redirect('administrator:departments')
    context = {'form':form}
    return render(request,'administrator/add_department.html',context=context)

@login_required(login_url='home:login')
 # edit department
def editDepartment(request,pk):
    if not request.user.is_superuser:
       return redirect('home:home')
    
    department = Departments.objects.get(pk=pk)
    if request.method == 'POST':
        form = CreateDepartments(request.POST,instance=department)
        if form.is_valid():
            form.save()
        else:
            messages.error(request,form.errors['name'])

    return redirect('administrator:departments')

@login_required(login_url='home:login')

def deleteDepartment(request,pk): # delete department
    if not request.user.is_superuser:
       return redirect('home:home')
    
    if request.method == 'POST':
        department = Departments.objects.get(pk=pk)
        if department.id != 1:
            users_department = userDepartment.objects.filter(department=department)
            for user_id in users_department:
                user = User.objects.get(pk=user_id.user.id)
                if not user.is_superuser:
                    user.delete()
            if department != None:
                department.delete()

    return redirect('administrator:departments')
#### end departments manager

#### user manager
@login_required(login_url='home:login')

def usersList(request): # show list users
    if not request.user.is_superuser:
       return redirect('home:home')

    sort  = request.GET.get('sort')
    if sort == None:
        sort = '-last_login'


    department_id = request.GET.get('department','')
    if len(department_id) > 0 :
        user_list_id = userDepartment.objects.filter(department_id = department_id).values_list('user',flat=True)
        filter = UsersFilter(request.GET, queryset=User.objects.filter(id__in=user_list_id).order_by(sort))
    else:
        filter = UsersFilter(request.GET, queryset=User.objects.all().order_by(sort))


    table = usersTable(filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=15)

    context = {'table':table,
               'filter':filter,
               'departments':Departments.objects.all()}
    
    return render(request,'administrator/users.html',context=context)

@login_required(login_url='home:login')

def addUser(request): # add user
    if not request.user.is_superuser:
       return redirect('home:home')
    
    if Departments.objects.all().count() == 0 :
        messages.warning(request,'You must have at least one Department to be able to add users')
        return redirect('administrator:departments/add')

    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data['password']
            department = form.cleaned_data['department']
            form = form.save(commit=False)
            form.password = make_password(pwd)
            form.save()
            department_ins = Departments.objects.get(name=department)
            userDepartment.objects.create(user=form,department=department_ins)
            if department_ins.id == 1:
                form.is_superuser = True
                form.save()
            messages.success(request,'Account created')
            return redirect('administrator:users')
        else:
            messages.error(request,form.errors)
    form = CreateUser()

    context = {'form':form}
    return render(request,'administrator/add_user.html',context=context)

@login_required(login_url='home:login')

def editUser(request,pk): # edit user
    if not request.user.is_superuser:
       return redirect('home:home')

    user_ins = User.objects.get(pk=pk)
    user_department = userDepartment.objects.get(user=user_ins)
    if user_ins.id == 1:
        messages.warning(request,'Admin account cannot be modified')
        return redirect('administrator:users')
  
    if request.method == 'POST':
        if user_ins.id == 1:
            messages.warning(request,'Admin account cannot be modified')
            return redirect('administrator:users')
        
        user_ins.username = request.POST.get('username')
        user_ins.first_name = request.POST.get('first_name')
        department_post = request.POST.get('department')

        
        if request.POST.get('password') != "":
            user_ins.password = make_password(request.POST.get('password'))
        
        department = Departments.objects.filter(pk=department_post)

        if department.exists():
            user_department.department  = department.first()
            user_department.save()
            if department.first().id == 1:
                user_ins.is_superuser = True
            else:
                user_ins.is_superuser = False
                
        if request.POST.get('is_active') == 'on':
            user_ins.is_active = True
        else:
            user_ins.is_active = False
        user_ins.save()
        messages.success(request,'Edit saved')
        return redirect('administrator:users')

    context = {'user_ins':user_ins,
               'departments':Departments.objects.all(),
               'user_department':user_department
               }
    return render(request,'administrator/user-edit.html', context)

@login_required(login_url='home:login')

def deleteUser(request,pk): # delete user
    if not request.user.is_superuser:
       return redirect('home:home')
    
    if request.method == 'POST':
        user = User.objects.get(pk=pk)
        if user.id != 1:
            user.delete()
            messages.success(request,'Account deleted')
        else:
            messages.warning(request,'The Admin account cannot be deleted')

    return redirect('administrator:users')
#### end user manager

#### records manager
@login_required(login_url='home:login')

def recordsDepartmentsList(request): # show records list
    if not request.user.is_superuser:
       return redirect('home:home')

    sort  = request.GET.get('sort')
    if sort == None:
        sort = '-date'

    filter = recordsFilter(request.GET, queryset=Records.objects.all().order_by(sort))
    table = recordsTableForAdmin(filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=15)
    
    export_format = request.GET.get("export", None)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table,dataset_kwargs={"title": "records"})
        return exporter.response(f"table.{export_format}")

    context = {'table':table,
               'filter': filter
               }
    return render(request,'administrator/records.html',context=context)

@login_required(login_url='home:login')

def recordsExtract(request): # extract records
    if not request.user.is_superuser:
       return redirect('home:home')

    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        download_method = request.POST.get('download_method')
        data = Records.objects.filter(date__gte=date_from,date__lte=date_to,is_validate=True).order_by('department')
        # Get verbose names of fields dynamically
        records_model = apps.get_model('users', 'Records')
        field_names = [records_model._meta.get_field(f'field_{i}').verbose_name for i in range(1, 11)]

        # Create an in-memory Excel file
        output = io.BytesIO()
        workbook = Workbook()
        sheet = workbook.active
        if  download_method == 'download_total_departments':
            departments = Departments.objects.exclude(pk=1).all().order_by('name')
            # Write column headers
            sheet.append(['Department Name'] + field_names + ['Total'])

            # Write data for each department
            for department in departments:
                department_data = [department.name]
                department_sum = 0
                for field_num in range(1, 11):
                    field_name = f'field_{field_num}'
                    field_sum = data.filter(department=department).aggregate(Sum(field_name))[f'{field_name}__sum']
                    field_sum = field_sum or 0  #  field_sum  0 if None
                    department_sum += field_sum
                    department_data.append(field_sum)
                department_data.append(department_sum)
                sheet.append(department_data)

            # Save the Excel file to the in-memory buffer
            workbook.save(output)

            # Prepare the response with the Excel file
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=download_total_departments.xlsx'
            response.write(output.getvalue())

            return response

        elif download_method == 'download_user_department':
            table = recordsTableForAdminExport(data)
            export_format = 'xlsx'
            if TableExport.is_valid_format(export_format):
                file_name="download_user_department"
                exporter = TableExport(export_format, table,dataset_kwargs={"title": file_name})
                return exporter.response(f"{file_name}.{export_format}")

        elif download_method == "download_total_records":
            # Write column headers
            sheet.append(field_names + ['Total'])

            # Calculate the total count of each field across all records
            field_totals = [data.aggregate(Sum(f'field_{i}'))[f'field_{i}__sum'] or 0 for i in range(1, 11)]
            total_count = sum(field_totals)

            # Write field totals to the Excel sheet
            sheet.append(field_totals + [total_count])

            # Save the Excel file to the in-memory buffer
            workbook.save(output)

            # Prepare the response with the Excel file
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=download_total_records.xlsx'
            response.write(output.getvalue())

            return response

    return render(request, 'administrator/extract.html')

@login_required(login_url='home:login')

def fileUploadedList(request): # show file upload list
    if not request.user.is_superuser:
       return redirect('home:home')
    sort  = request.GET.get('sort')
    if sort == None:
        sort = '-date'
    filter = fileUploadedFilter(request.GET, queryset=uploadFile.objects.all().order_by(sort))
    table = uploadFileTableForAdmin(filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=15)

    export_format = request.GET.get("export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table,dataset_kwargs={"title": "records"})
        return exporter.response(f"table.{export_format}")

    context = {'table':table,
               'filter':filter}
    return render(request,'administrator/file-uploaded.html',context=context)


#### end records manager