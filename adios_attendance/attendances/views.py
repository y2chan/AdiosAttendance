from django.shortcuts import render, redirect
from datetime import date
from .forms import SignUpForm, AttendanceForm
from .models import Student, Attendance
from django.contrib.auth import authenticate, login as auth_login
import logging

logger = logging.getLogger(__name__)

def user_login(request):
    if request.method == 'POST':
        student_id = request.POST['student_id']
        name = request.POST['name']
        user = authenticate(request, username=student_id, password=name)

        if user is not None:
            # 로그인 성공 시 세션에 student_id를 저장
            request.session['student_id'] = student_id
            auth_login(request, user)
            logger.info(f"User '{student_id}' logged in.")
            logger.info(f"Session student_id_in_session: {request.session.get('student_id')}")
            return redirect('dashboard')  # 로그인 성공 시 대시보드로 리디렉션
        else:
            error_message = '학번 또는 이름이 잘못되었습니다.'
            logger.warning(f"Login failed for student_id '{student_id}'.")
            logger.info(f"Session student_id_in_session: {request.session.get('student_id')}")
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def dashboard(request):
    student_id_in_session = request.session.get('student_id')
    student_from_session = Student.objects.filter(pk=student_id_in_session).first()
    print('student_id_in_session:', student_id_in_session)
    print('student_from_session:', student_from_session)

    if not request.user.is_authenticated:
        return redirect('login')  # 로그인되지 않은 사용자는 로그인 페이지로 리디렉션

    student = request.user.student
    todays_attendance = student.attendance_set.filter(date=date.today()).exists()

    form = AttendanceForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    attendance_records = Attendance.objects.filter(student=student).order_by('-date')
    all_students = Student.objects.all()

    for student in all_students:
        student.attendance_status = "출석" if student.attendance_set.filter(date=date.today()).exists() else "결석"

    context = {
        'student': student,
        'todays_attendance': todays_attendance,
        'form': form,
        'attendance_records': attendance_records,
        'all_students': all_students,
    }

    return render(request, 'dashboard.html', context)

def check_in(request):

    if 'student_id' not in request.session:
        return redirect('login')

    student = Student.objects.get(pk=request.session['student_id'])
    if not Attendance.objects.filter(student=student, date=date.today()).exists():
        Attendance.objects.create(student=student, date=date.today())

    return redirect('dashboard')

def attendance_list(request):
    if 'student_id' not in request.session:
        return redirect('login')

    student = Student.objects.get(pk=request.session['student_id'])
    attendance_records = Attendance.objects.filter(student=student).order_by('date')
    return render(request, 'attendance_list.html', {'student': student, 'attendance_records': attendance_records})

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
        student.attendance_status = "출석" if student.attendance_set.filter(date=date.today()).exists() else "결석"

    return render(request, 'all_attendance_list.html', {'students': students})


