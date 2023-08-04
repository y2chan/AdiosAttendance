from django import forms
from .models import Student, Attendance, AvailableDate, PracticeAvailable, PracticeDateDetail, Notice
from django.contrib import messages

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

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        if len(str(student_id)) != 10:
            raise forms.ValidationError('학번은 10자리 숫자여야 합니다.')
        return student_id

    def clean_name(self):
        name = self.cleaned_data['name']
        existing_names = Student.objects.filter(name=name)
        if existing_names.exists():
            raise forms.ValidationError('같은 이름이 존재합니다.')
        if not (2 <= len(name) <= 3 and name.isalpha()):
            raise forms.ValidationError('이름은 2~3자리 한글로 입력해야 합니다.')
        return name

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['user', 'date', 'is_attending']

class LoginForm(forms.Form):
    student_id = forms.CharField(label='학번', max_length=10)
    name = forms.CharField(label='이름', max_length=50)

class DateForm(forms.ModelForm):
    class Meta:
        model = AvailableDate
        fields = ['date', 'content']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'content': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'date': '날짜',
            'content': '내용'
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_suffix = ''

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(str(content)) > 200:
            raise forms.ValidationError('내용은 200자 이내로 제한합니다.')
        return content

from django import forms
from .models import PracticeAvailable
from django.contrib.auth import get_user_model

from django import forms
from .models import PracticeAvailable

class PracticeAvailableForm(forms.ModelForm):
    class Meta:
        model = PracticeAvailable
        fields = ['date', 'content']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'content': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'date': '연습 불가 날짜',
            'content': '사유',
        }

    def __init__(self, *args, **kwargs):
        super(PracticeAvailableForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.label_suffix = ''

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(str(content)) > 200:
            raise forms.ValidationError('내용은 200자 이내로 제한합니다.')
        return content


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

    def clean_content(self):
        content = self.cleaned_data['content']
        if len(str(content)) > 200:
            raise forms.ValidationError('내용은 200자 이내로 제한합니다.')
        return content