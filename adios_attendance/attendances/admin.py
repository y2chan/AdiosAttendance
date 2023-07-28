from django.contrib import admin
from .models import Student, Attendance

# 모델을 관리자 페이지에 등록합니다.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date')

