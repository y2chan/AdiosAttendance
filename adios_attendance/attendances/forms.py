from django import forms
from .models import Student, AvailableDate

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id','name']

class AttendanceForm(forms.Form):
    # 출석 체크에 필요한 필드들을 여기에 추가합니다
    # 예: date = forms.DateField()
    pass

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