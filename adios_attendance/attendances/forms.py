from django import forms
from .models import Student, Attendance, AvailableDate, PracticeAvailable, PracticeDateDetail, Notice

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name']
        labels = {
            'student_id': '학번',
            'name': '이름',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['user', 'available_date', 'is_attending']

class LoginForm(forms.Form):
    student_id = forms.CharField(label='학번', max_length=10)
    name = forms.CharField(label='이름', max_length=50)

class DateForm(forms.ModelForm):
    class Meta:
        model = AvailableDate
        fields = ['name', 'date', 'content']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'content': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'name': '이름',
            'date': '날짜',
            'content': '내용'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''

class PracticeAvailableForm(forms.ModelForm):
    class Meta:
        model = PracticeAvailable
        fields = ['student', 'title', 'date', 'content']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'content': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'student': '작성자',
            'title': '제목',
            'date': '연습 불가 날짜',
            'content': '사유'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''

class PracticeDateDetailForm(forms.ModelForm):
    class Meta:
        model = PracticeDateDetail
        fields = ['practice_date', 'user', 'is_attending']

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content']
        labels = {
                    'title': '제목',
                    'content': '내용'
                }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''