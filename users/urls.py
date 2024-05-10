from django.urls import path
from . import views
app_name="users"

urlpatterns = [
    path('records',views.recordsList,name='records'),
    path('record/add',views.addRecord,name='record/add'),
    path('record/show/<pk>',views.showRecord,name='record/show'),
    path('record/edit/<pk>',views.editRecord,name='record/edit'),
    path('record/delete/<pk>',views.deleteRecord,name='record/delete'),
    path('upload-file',views.addUploadFile,name='upload-file'),
    path('upload-file/edit/<pk>',views.editUploadFile,name='upload-file/edit/'),
    path('upload-file/show/<pk>',views.showUploadFile,name='upload-file/show/'),
    path('upload-file/delete/<pk>',views.deleteUploadFile,name='upload-file/delete/'),
]
