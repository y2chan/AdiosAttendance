from django import forms
from .models import Student

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name']

class AttendanceForm(forms.Form):
    # 출석 체크에 필요한 필드들을 여기에 추가합니다
    # 예: date = forms.DateField()
    pass