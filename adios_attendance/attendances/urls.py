from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),  # 대시보드로 접속하는 URL 패턴 추가
    path('check_in/', views.check_in, name='check_in'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('signup/', views.signup, name='signup'),
    path('all_attendance_list/', views.all_attendance_list, name='all_attendance_list'),
    path('login/', views.user_login, name='login'),  # 로그인 뷰 함수를 urlpatterns에 등록
]