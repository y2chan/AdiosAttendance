from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'attendances'

urlpatterns = [
    path('', views.home, name='home'),  # 첫 화면 뷰
    path('user_login/', views.user_login, name='user_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('check_in/', views.check_in, name='check_in'),
    path('attendance_list/', views.attendance_list, name='attendance_list'),
    path('signup/', views.signup, name='signup'),
    path('all_attendance_list/', views.all_attendance_list, name='all_attendance_list'),
    path('notice/', views.notice, name='notice'),
    path('notice/<int:notice_id>', views.notice_detail, name='notice_detail'),
    path('notice/add/', views.notice_add, name='notice_add'),
    path('notice/<int:notice_id>/delete/', views.notice_delete, name='notice_delete'),
    path('practice_date/', views.practice_date_list, name='practice_date_list'),
    path('practice_date/add', views.practice_date, name='practice_date'),
    path('practice_date/<int:pk>/', views.practice_date_detail, name='practice_date_detail'),
    path('practice_date/<int:available_date_id>/update_attendance_status/', views.update_attendance_status, name='update_attendance_status'),
    path('practice_date/<int:pk>/delete/', views.delete_practice_date_detail, name='delete_practice_date_detail'),
    path('practice_available/', views.practice_available_list, name='practice_available_list'),
    path('practice_available/<int:practice_available_id>', views.practice_available_detail, name='practice_available_detail'),
    path('practice_available/add/', views.practice_available_add, name='practice_available_add'),
    path('practice_available/<int:pk>/delete/', views.delete_practice_available, name='delete_practice_available')

]