from django.urls import path
from . import views

app_name="home"

urlpatterns = [
    path('',views.home,name='home'),
    path('about',views.about,name='about'),
    path('login',views.user_login,name='login'),
    path('logout',views.logout,name='logout'),
]
