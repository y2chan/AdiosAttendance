from django.shortcuts import render, redirect
from datetime import date
from .forms import SignUpForm, AttendanceForm, LoginForm, DateForm
from .models import Student, Attendance, Notice, PracticeAvailable, AvailableDate
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
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
        return redirect('attendances:dashboard')

    return render(request, 'login.html')


def dashboard(request):
    student_id_in_session = request.session.get('student_id')
    student_from_session = Student.objects.filter(student_id=student_id_in_session).first()

    if not student_from_session:
        return redirect('attendances:login')  # 로그인되지 않은 사용자는 로그인 페이지로 리디렉션

    todays_attendance = student_from_session.attendance_set.filter(date=date.today()).exists()

    form = AttendanceForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # 폼에 학생 정보를 저장한 후 현재 날짜로 출결 정보를 저장합니다.
            attendance = form.save(commit=False)
            attendance.student_id = student_from_session.student_id
            attendance.date = date.today()
            attendance.save()
            return redirect('attendances:dashboard')

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
        return redirect('attendances:login')

    student_id = request.session['student_id']
    student = Student.objects.get(student_id=student_id)  # 해당 학생의 Student 모델 인스턴스를 가져옴

    if not Attendance.objects.filter(student=student, date=date.today()).exists():
        Attendance.objects.create(student=student, date=date.today())

    return redirect('attendances:dashboard')


def attendance_list(request):
    if 'student_id' not in request.session:
        return redirect('attendances:login')

    student_id = request.session['student_id']
    student = Student.objects.get(student_id=student_id)
    attendance_records = Attendance.objects.filter(student_id=student_id).order_by('-date')  # 날짜 기준으로 내림차순 정렬
    return render(request, 'attendance_list.html', {'student': student, 'attendance_records': attendance_records})




def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendances:login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def all_attendance_list(request):
    student_id_in_session = request.session.get('student_id')
    student_from_session = Student.objects.filter(student_id=student_id_in_session).first()

    form = AttendanceForm(request.POST or None)

    if not student_from_session:
        return redirect('attendances:login')

    if request.method == 'POST':
        if form.is_valid():
            # 폼에 학생 정보를 저장한 후 현재 날짜로 출결 정보를 저장합니다.
            attendance = form.save(commit=False)
            attendance.student_id = student_from_session.student_id
            attendance.date = date.today()
            attendance.save()
            return redirect('attendances:dashboard')

    todays_attendance = student_from_session.attendance_set.filter(date=date.today()).exists()
    all_students = Student.objects.all()

    # 모든 학생들의 출결 상태를 업데이트합니다.
    for student in all_students:
        student.attendance_status = "출석" if student.attendance_set.filter(date=date.today()).exists() else "결석"

    return render(request, 'all_attendance_list.html', {'student': student_from_session, 'all_students': all_students})


def notice(request):
    now = timezone.now()

    # 최근 1달 내의 시간 (현재 시간에서 1달 전의 시간)
    one_month_ago = now - timezone.timedelta(days=30)

    # 최근 1달 내의 공지만 가져옴
    notices = Notice.objects.filter(created_at__gte=one_month_ago).order_by('-created_at')

    context = {
        'notices': notices,
    }

    return render(request, 'notice.html', context)

def notice_add(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        # 공지사항 등록을 위한 데이터 처리 로직 작성
        # 필요에 따라 Notice 모델을 사용해서 데이터베이스에 저장
        return redirect('attendances:notice')  # 공지사항 목록 페이지로 리디렉션

    return render(request, 'notice_add.html')

def practice_date(request):
    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            content = form.cleaned_data['content']
            AvailableDate.objects.create(name=name, date=date, content=content)
            return redirect('attendances:practice_date_list')
    else:
        form = DateForm()

    return render(request, 'practice_date.html', {'form': form})


def practice_date_list(request):
    available_dates = AvailableDate.objects.all().order_by('-date')
    return render(request, 'practice_date_list.html', {'available_dates': available_dates})

def practice_available_list(request):
    practice_availables = PracticeAvailable.objects.all().order_by('-created_date')
    return render(request, 'practice_available_list.html', {'practice_availables': practice_availables})

def practice_available_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['date']
        content = request.POST['content']
        PracticeAvailable.objects.create(name=name, date=date, content=content)
        return redirect('attendances:practice_available_list')

    return render(request, 'practice_available_add.html')


