from django.shortcuts import render, redirect
from datetime import date
from .forms import SignUpForm, AttendanceForm, LoginForm
from .models import Student, Attendance
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)


def user_login(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        name = request.POST.get('name')

        User = get_user_model()
        try:
            user = User.objects.get(student_id=student_id, name=name)
        except User.DoesNotExist:
            # 사용자가 존재하지 않는 경우
            error_message = '학번 또는 이름이 잘못되었습니다.'
            messages.error(request, error_message)
            return redirect('login')

        # 로그인 처리
        request.session['student_id'] = user.student_id
        request.session['name'] = user.name

        # 로그인 성공 시 대시보드로 리디렉션
        return redirect('dashboard')

    return render(request, 'login.html')


def dashboard(request):
    student_id_in_session = request.session.get('student_id')
    student_from_session = Student.objects.filter(student_id=student_id_in_session).first()

    if not student_from_session:
        return redirect('login')  # 로그인되지 않은 사용자는 로그인 페이지로 리디렉션

    todays_attendance = student_from_session.attendance_set.filter(date=date.today()).exists()

    form = AttendanceForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # 폼에 학생 정보를 저장한 후 현재 날짜로 출결 정보를 저장합니다.
            attendance = form.save(commit=False)
            attendance.student_id = student_from_session.student_id
            attendance.date = date.today()
            attendance.save()
            return redirect('dashboard')

    attendance_records = Attendance.objects.filter(student_id=student_from_session.student_id).order_by('-date')
    all_students = Student.objects.all()

    # 모든 학생들의 출결 상태를 업데이트합니다.
    for student in all_students:
        student.attendance_status = "출석" if student.attendance_set.filter(date=date.today()).exists() else "결석"

    context = {
        'student': student_from_session,
        'todays_attendance': todays_attendance,
        'form': form,
        'attendance_records': attendance_records,
        'all_students': all_students,
    }

    return render(request, 'dashboard.html', context)




def check_in(request):
    if 'student_id' not in request.session:
        return redirect('login')

    student_id = request.session['student_id']
    if not Attendance.objects.filter(student_id=student_id, date=date.today()).exists():
        Attendance.objects.create(student_id=student_id, date=date.today())

    return redirect('dashboard')


def attendance_list(request):
    if 'student_id' not in request.session:
        return redirect('login')

    student_id = request.session['student_id']
    attendance_records = Attendance.objects.filter(student_id=student_id).order_by('date')
    return render(request, 'attendance_list.html', {'attendance_records': attendance_records})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def all_attendance_list(request):
    students = Student.objects.all()

    for student in students:
        student.attendance_status = "출석" if Attendance.objects.filter(student_id=student.student_id, date=date.today()).exists() else "결석"

    return render(request, 'all_attendance_list.html', {'students': students})



