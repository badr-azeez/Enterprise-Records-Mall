from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from administrator.models import Departments  ,userDepartment
class Command(BaseCommand):
    help = 'create admin and adminsGroup'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            ## create super user
            user = User.objects.create_superuser('admin', 'admin@domain.com', 'password',first_name="admin site")
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))

            ## create admin group
            department = Departments.objects.create(name='admin group')
            self.stdout.write(self.style.SUCCESS('Admin Group created successfully'))

            ## add super user to admin
            userDepartment.objects.create(department=department,user=user)
            self.stdout.write(self.style.SUCCESS('Super User added to Admin Group successfully'))
            
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
