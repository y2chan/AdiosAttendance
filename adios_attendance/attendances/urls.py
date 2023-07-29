from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),  # 첫 페이지로 로그인 뷰를 사용합니다.
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('check_in/', views.check_in, name='check_in'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('signup/', views.signup, name='signup'),
    path('all_attendance_list/', views.all_attendance_list, name='all_attendance_list'),
]

app_name = 'attendance'