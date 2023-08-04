from django.shortcuts import render, redirect, get_object_or_404
from datetime import date, timedelta, datetime
from .forms import SignUpForm, AttendanceForm, LoginForm, DateForm, PracticeAvailableForm, NoticeForm
from .models import Student, Attendance, Notice, PracticeAvailable, AvailableDate, PracticeDateDetail
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.paginator import Paginator, Page
from functools import wraps
from django.db.models import Q
import logging


logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'home.html')

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
            return redirect('attendances:user_login')

        # 로그인 처리
        request.session['student_id'] = user.student_id
        request.session['name'] = user.name

        # 로그인 성공 시 대시보드로 리디렉션
        return redirect('attendances:dashboard')

    return render(request, 'login.html',)


def dashboard(request):
    student_id_in_session = request.session.get('student_id')
    student_from_session = Student.objects.filter(student_id=student_id_in_session).first()

    if not student_from_session:
        return redirect('attendances:user_login')

    # 현재 날짜의 출결 정보가 있는지 확인
    todays_attendance = Attendance.objects.filter(user=student_from_session, date=date.today()).exists()

    form = AttendanceForm(request.POST or None)
    thousand_days_date = date(2023, 10, 4)
    sept_twelve_date = date(2023, 9, 12)
    today = date.today()
    days_left_to_sept_twelve = (sept_twelve_date - today).days
    days_left_to_thousand_days = (thousand_days_date - today).days

    if days_left_to_sept_twelve > 0:
        message = f"동아리 박람회까지 {days_left_to_sept_twelve}일 남았다!!!"
    elif days_left_to_thousand_days > 0:
        message = f"천보축전까지 {days_left_to_thousand_days}일 남았다!!!"
    else:
        message = "고생했다 얘들아!!!"

    if request.method == 'POST':
        if form.is_valid():
            # 폼에 학생 정보를 저장한 후 현재 날짜로 출결 정보를 저장합니다.
            attendance = form.save(commit=False)
            attendance.student_id = student_from_session.student_id
            attendance.available_date = AvailableDate.objects.get(date=date.today())
            attendance.save()
            return redirect('attendances:dashboard')

    # 학생의 출결 기록을 가져옵니다. user 필드를 사용하고, available_date__date를 기준으로 내림차순 정렬합니다.
    attendance_records = Attendance.objects.filter(user=student_from_session).order_by('-date')
    all_students = Student.objects.all()

    # 모든 학생들의 출결 상태를 업데이트합니다. available_date__date를 기준으로 상태를 업데이트하도록 변경하였습니다.
    for student in all_students:
        student.attendance_status = "출석" if student.attendance_set.filter(date=date.today()).exists() else "결석"

    context = {
        'student': student_from_session,
        'todays_attendance': todays_attendance,
        'form': form,
        'attendance_records': attendance_records,
        'all_students': all_students,
        'todays_attendance': todays_attendance,
        'message': message,
        'days_left_to_sept_twelve': days_left_to_sept_twelve,
        'days_left_to_thousand_days' : days_left_to_thousand_days
    }

    return render(request, 'dashboard.html', context)

from datetime import date

def check_in(request):
    if 'student_id' not in request.session:
        return redirect('attendances:user_login')

    student_id = request.session['student_id']
    student = Student.objects.get(student_id=student_id)

    # 오늘 날짜를 가져와서 출석 정보를 확인합니다.
    today = date.today()
    try:
        today_attendance = Attendance.objects.get(user=student, date=today)
    except Attendance.DoesNotExist:
        # 출석 정보가 없으면 생성합니다.
        today_attendance = Attendance.objects.create(user=student, date=today)

    return redirect('attendances:dashboard')

from datetime import date, timedelta

def get_this_week_range():
    today = date.today()
    start_date = today - timedelta(days=today.weekday())
    end_date = start_date + timedelta(days=6)
    return start_date, end_date, today.weekday()


def analyze_attendance_per_week(attendance_records, today_weekday):
    analyzed_data = {}
    current_date = date.today()
    one_week = timedelta(days=7)

    # 최대 5주치의 데이터를 분석합니다.
    for week_number in range(5):
        start_date = current_date - timedelta(days=(today_weekday + 1))  # 현재 주의 월요일로 설정
        end_date = start_date + timedelta(days=6)  # 현재 주의 일요일로 설정

        # 해당 주에 출석한 횟수를 세어 analyzed_data에 추가합니다.
        weekly_attendance_count = attendance_records.filter(date__range=[start_date, end_date]).count()
        analyzed_data[week_number] = {
            'count': weekly_attendance_count,
            'start_date': start_date,
            'end_date': end_date,
        }

        current_date -= one_week  # 이전 주로 이동

    return analyzed_data


def attendance_list(request):
    if 'student_id' not in request.session:
        return redirect('attendances:user_login')

    student_id = request.session['student_id']
    student = Student.objects.get(student_id=student_id)

    # 해당 학생의 출석 기록을 가져옵니다.
    attendance_records = Attendance.objects.filter(user=student).order_by('-date')

    # 이번 주 기간과 오늘의 요일을 가져옵니다.
    start_date, end_date, today_weekday = get_this_week_range()

    # 해당 학생의 이번 주 출석 기록을 가져옵니다.
    this_week_attendance_records = attendance_records.filter(date__range=[start_date, end_date])

    # 이번 주 출석 횟수를 세는 함수를 호출하여 분석합니다.
    analyzed_attendance = analyze_attendance_per_week(this_week_attendance_records, today_weekday)

    return render(request, 'attendance_list.html', {'student': student, 'attendance_records': this_week_attendance_records, 'analyzed_attendance': analyzed_attendance})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendances:user_login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def all_attendance_list(request):
    student_id_in_session = request.session.get('student_id')
    student_from_session = Student.objects.filter(student_id=student_id_in_session).first()

    if not student_from_session:
        return redirect('attendances:user_login')

    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except ValueError:
            # 잘못된 형식의 날짜가 입력된 경우 오늘 날짜로 설정
            selected_date = date.today()
    else:
        selected_date = date.today()

    all_students = Student.objects.all()

    # 모든 학생들의 출결 상태를 업데이트합니다.
    for student in all_students:
        attendance_status = "출석" if student.attendance_set.filter(date=selected_date).exists() else "결석"
        setattr(student, 'attendance_status', attendance_status)

    # 선택한 날짜의 출석과 결석한 학생들을 필터링합니다.
    attendance_present_students = [student for student in all_students if student.attendance_status == "출석"]
    attendance_absent_students = [student for student in all_students if student.attendance_status == "결석"]

    return render(request, 'all_attendance_list.html', {
        'student': student_from_session,
        'all_students': all_students,
        'attendance_present_students': attendance_present_students,
        'attendance_absent_students': attendance_absent_students,
        'selected_date': selected_date_str,
    })

def notice(request):
    query = request.GET.get('q')
    base_notices = Notice.objects.all().order_by('-created_at')  # 기본적으로 모든 공지사항을 날짜 역순으로 정렬

    if query:
        filtered_notices = base_notices.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_at')
    else:
        filtered_notices = base_notices

    paginator = Paginator(filtered_notices, 4)  # 한 페이지에 4개의 공지사항을 보여줍니다.
    page_number = request.GET.get('page')
    notices = paginator.get_page(page_number)

    current_page_range = get_page_range_notice(notices)

    context = {
        'notices': notices,
        'current_page_range': current_page_range,
        'query': query
    }

    return render(request, 'notice.html', context)

def get_page_range_notice(page_obj, num_pages_to_show=10):
    current_index = page_obj.number - 1
    num_pages = page_obj.paginator.num_pages

    if num_pages <= num_pages_to_show:
        page_range = list(range(1, num_pages + 1))
    else:
        num_middle_pages = num_pages_to_show - 2
        half_num_middle_pages = num_middle_pages // 2

        if current_index <= half_num_middle_pages:
            page_range = list(range(1, num_pages_to_show))
        elif current_index >= num_pages - half_num_middle_pages - 1:
            page_range = list(range(num_pages - num_pages_to_show + 1, num_pages + 1))
        else:
            start_index = current_index - half_num_middle_pages
            end_index = current_index + half_num_middle_pages + 1
            page_range = list(range(start_index + 1, end_index))

    return page_range

from django.utils import timezone

def notice_add(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        # 공지사항 등록을 위한 데이터 처리 로직 작성
        # 필요에 따라 Notice 모델을 사용해서 데이터베이스에 저장
        # created_at 필드에 현재 시간 설정
        notice = Notice.objects.create(title=title, content=content, created_at=timezone.now())

        return redirect('attendances:notice')  # 공지사항 목록 페이지로 리디렉션

    return render(request, 'notice_add.html')

def notice_delete(request, notice_id):
     notice = get_object_or_404(Notice, id=notice_id)

     if request.method == 'POST':
         notice.delete()
         return redirect('attendances:notice')  # 공지사항 목록 페이지로 리디렉션

     return render(request, 'notice_delete.html', {'notice': notice})

def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('attendances:notice')  # Redirect to the notice list page

    else:
        form = NoticeForm(instance=notice)

    return render(request, 'notice_detail.html', {'form': form, 'notice': notice})

def practice_date(request):
    # 세션에서 현재 로그인한 사용자 이름 가져오기
    current_user_name = request.session.get('name')

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(Student, name=current_user_name)
            practice_date = form.save(commit=False)
            practice_date.name = user
            practice_date.save()

            return redirect('attendances:practice_date_list')
    else:
        form = DateForm()

    return render(request, 'practice_date.html', {'form': form})


def practice_date_list(request):
    query = request.GET.get('q')
    available_dates = AvailableDate.objects.all().order_by('-date')
    selected_post = None

    if request.method == 'POST':
        for date in available_dates:
            is_attending = request.POST.get(str(date.date), False)
            date.is_attending = is_attending
            date.save()

        selected_post_id = request.POST.get('selected_post')
        if selected_post_id:
            selected_post = AvailableDate.objects.get(id=selected_post_id)

    if query:
        filtered_available_dates = available_dates.filter(Q(content__icontains=query) | Q(name__icontains=query) | Q(date__icontains=query)).order_by('-date')
    else:
        filtered_available_dates = available_dates

    paginator = Paginator(filtered_available_dates, 4)  # 한 페이지에 4개의 게시물을 보여줍니다.
    page_number = request.GET.get('page')
    vote = paginator.get_page(page_number)

    # 이 부분에서 추가적인 context 변수를 전달합니다.
    current_page_range = get_page_range_vote(vote)

    context = {
        'available_dates': filtered_available_dates,
        'selected_post': selected_post,
        'vote': vote,
        'current_page_range': current_page_range,
    }

    return render(request, 'practice_date_list.html', context)

def get_page_range_vote(page_obj, num_pages_to_show=10):
    current_index = page_obj.number - 1
    num_pages = page_obj.paginator.num_pages

    if num_pages <= num_pages_to_show:
        page_range = list(range(1, num_pages + 1))
    else:
        num_middle_pages = num_pages_to_show - 2
        half_num_middle_pages = num_middle_pages // 2

        if current_index <= half_num_middle_pages:
            page_range = list(range(1, num_pages_to_show))
        elif current_index >= num_pages - half_num_middle_pages - 1:
            page_range = list(range(num_pages - num_pages_to_show + 1, num_pages + 1))
        else:
            start_index = current_index - half_num_middle_pages
            end_index = current_index + half_num_middle_pages + 1
            page_range = list(range(start_index + 1, end_index))

    return page_range

from django.utils import timezone

def practice_date_detail(request, pk):
    # 세션에서 로그인 정보 가져오기
    student_id = request.session.get('student_id')
    name = request.session.get('name')

    # 로그인 정보가 없다면 로그인 페이지로 리디렉션
    if not student_id or not name:
        return redirect('attendances:user_login')

    # 세션에서 가져온 로그인 정보로 사용자 객체 가져오기
    User = get_user_model()
    try:
        user = User.objects.get(student_id=student_id, name=name)
    except User.DoesNotExist:
        # 사용자가 존재하지 않는 경우
        error_message = '학번 또는 이름이 잘못되었습니다.'
        messages.error(request, error_message)
        return redirect('attendances:user_login')

    # pk가 None인 경우에는 selected_post를 None으로 설정
    selected_post = None
    if pk is not None:
        selected_post = get_object_or_404(AvailableDate, pk=pk)

    # 해당 연습 일정에 대한 참가자, 불참자, 비투표자 목록 조회
    attendees = PracticeDateDetail.objects.filter(practice_date=selected_post, is_attending=True)
    non_attendees = PracticeDateDetail.objects.filter(practice_date=selected_post, is_attending=False)
    unvoted_users = User.objects.exclude(practicedatedetail__practice_date=selected_post)

    # 현재 로그인한 사용자의 투표 여부 정보 가져오기
    user_vote = None
    if selected_post:
        try:
            user_vote = PracticeDateDetail.objects.get(practice_date=selected_post, user=user)
        except PracticeDateDetail.DoesNotExist:
            user_vote = None

    context = {
        'selected_post': selected_post,
        'attendees': attendees,
        'non_attendees': non_attendees,
        'unvoted_users': unvoted_users,
        'user_vote': user_vote,  # 현재 사용자의 투표 정보를 전달
    }

    return render(request, 'practice_date_detail.html', context)

from django.shortcuts import get_object_or_404

def update_attendance_status(request, available_date_id):
    student_id = request.session.get('student_id')

    if request.method == 'POST':
        # AvailableDate 객체 가져오기
        practice_date = get_object_or_404(AvailableDate, pk=available_date_id)

        # 세션에서 읽어온 student_id를 사용하여 해당 사용자를 가져옵니다.
        # student_id가 없으면 사용자가 로그인되어 있지 않으므로 로그인 페이지로 리디렉션합니다.
        if not student_id:
            return redirect('attendances:user_login')

        # student_id를 사용하여 해당 사용자를 가져옵니다.
        # student_id가 유효한지 확인하는 것이 중요합니다.
        # 예를 들어, 잘못된 student_id를 사용하려는 시도 등을 방지해야 합니다.
        user = get_object_or_404(Student, student_id=student_id)

        # 수정된 부분: request.POST.get('is_attending')를 불리언 값으로 변환
        is_attending = request.POST.get('is_attending') == 'True'

        # PracticeDateDetail 객체 생성 또는 업데이트
        try:
            practice_date_detail = PracticeDateDetail.objects.get(practice_date=practice_date, user=user)
            practice_date_detail.is_attending = is_attending
            practice_date_detail.save()
        except PracticeDateDetail.DoesNotExist:
            PracticeDateDetail.objects.create(practice_date=practice_date, user=user, is_attending=is_attending)

        messages.success(request, '참가 여부가 업데이트 되었습니다.')
        return redirect('attendances:practice_date_detail', pk=available_date_id)

    return redirect('attendances:practice_date_detail', pk=available_date_id)

def delete_practice_date_detail(request, pk):
    practice_date_detail = get_object_or_404(AvailableDate, pk=pk)

    if request.method == 'POST':
        # POST 요청일 때만 삭제를 수행합니다.
        practice_date_detail.delete()
        messages.success(request, '투표가 삭제되었습니다.')
        return redirect('attendances:practice_date_list')

    # POST 요청이 아닌 경우, 해당 연습 일정 상세 페이지로 리디렉션합니다.
    return redirect('attendances:practice_date_detail', pk=pk)

def practice_available_list(request):
    query = request.GET.get('q')
    practice_availables = PracticeAvailable.objects.all().order_by('-created_date')

    if query:
        filtered_practice_availables = practice_availables.filter(Q(content__icontains=query) | Q(student__name__icontains=query) | Q(date__icontains=query)).order_by('-date')
    else:
        filtered_practice_availables = practice_availables
    paginator = Paginator(filtered_practice_availables, 4)  # 한 페이지에 4개의 게시물을 보여줍니다.
    page_number = request.GET.get('page')
    availables = paginator.get_page(page_number)

    # 이 부분에서 추가적인 context 변수를 전달합니다.
    current_page_range = get_page_range_practice(availables)

    context = {
            'availables': filtered_practice_availables,
            'current_page_range': current_page_range,
            'query': query
        }

    return render(request, 'practice_available_list.html', context)

def get_page_range_practice(page_obj, num_pages_to_show=10):
    current_index = page_obj.number - 1
    num_pages = page_obj.paginator.num_pages

    if num_pages <= num_pages_to_show:
        page_range = list(range(1, num_pages + 1))
    else:
        num_middle_pages = num_pages_to_show - 2
        half_num_middle_pages = num_middle_pages // 2

        if current_index <= half_num_middle_pages:
            page_range = list(range(1, num_pages_to_show))
        elif current_index >= num_pages - half_num_middle_pages - 1:
            page_range = list(range(num_pages - num_pages_to_show + 1, num_pages + 1))
        else:
            start_index = current_index - half_num_middle_pages
            end_index = current_index + half_num_middle_pages + 1
            page_range = list(range(start_index + 1, end_index))

    return page_range

def practice_available_detail(request, practice_available_id):
    practice_available = get_object_or_404(PracticeAvailable, id=practice_available_id)

    if request.method == 'POST':
        form = PracticeAvailableForm(request.POST, instance=practice_available)
        if form.is_valid():
            form.save()
            return redirect('attendances:practice_available_list')
    else:
        form = PracticeAvailableForm(instance=practice_available)

    return render(request, 'practice_available_detail.html', {'form': form, 'practice_available': practice_available})

def delete_practice_available(request, pk):
    try:
        practice_available = PracticeAvailable.objects.get(pk=pk)
        practice_available.delete()
    except PracticeAvailable.DoesNotExist:
        pass  # 해당 게시물이 존재하지 않는 경우

    return redirect('attendances:practice_available_list')


def practice_available_add(request):
    # 세션에서 현재 로그인한 사용자 이름 가져오기
    current_user_name = request.session.get('name')

    if request.method == 'POST':
        form = PracticeAvailableForm(request.POST)
        if form.is_valid():
            # 현재 로그인한 사용자 정보를 가져와서 student 필드에 저장
            user = get_object_or_404(Student, name=current_user_name)
            practice_available = form.save(commit=False)
            practice_available.student = user
            practice_available.save()

            return redirect('attendances:practice_available_list')
    else:
        form = PracticeAvailableForm()

    return render(request, 'practice_available_add.html', {'form': form})


