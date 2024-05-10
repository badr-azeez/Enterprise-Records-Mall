from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

year = datetime.today().year
month = datetime.today().month
day = datetime.today().day


class Departments(models.Model):
    name = models.CharField(max_length=100,unique=True,verbose_name="department")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="added at")
    last_modified = models.DateTimeField(auto_now=True, verbose_name="modified at")

    def __str__(self):
        return self.name

class userDepartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user')
    department = models.ForeignKey(Departments, on_delete=models.CASCADE,related_name='department')