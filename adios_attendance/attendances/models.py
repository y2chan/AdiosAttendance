from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, student_id, name, password=None):
        if not student_id:
            raise ValueError("The Student ID must be set")
        if not name:
            raise ValueError("The Name must be set")

        user = self.model(student_id=student_id, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, student_id, name, password=None):
        user = self.create_user(student_id, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Student(AbstractUser):
    username = None  # We are using student_id as the username field, so we set username to None
    student_id = models.CharField(max_length=10, unique=True, verbose_name='Student ID')
    name = models.CharField(max_length=50, verbose_name='Name')

    USERNAME_FIELD = 'student_id'  # Set 'student_id' as the field for authentication
    REQUIRED_FIELDS = ['name']  # Add 'name' to the required fields for createsuperuser

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.student_id} - {self.name}"

class AvailableDate(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    content = models.TextField(default='')
    created_date = models.DateTimeField(auto_now_add=True)
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Attendance')

    def __str__(self):
         return f"{self.name} - {self.date}"

class Attendance(models.Model):
    # 각 참가자들의 연습 일정과 관련된 정보를 저장
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    available_date = models.ForeignKey(AvailableDate, on_delete=models.CASCADE)
    is_attending = models.BooleanField(default=False)
    # id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.user.username} - {self.available_date}"

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class PracticeAvailable(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, default='')
    title = models.CharField(max_length=100)  # title 필드의 모델에서 CharField로 변경
    date = models.DateField()
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date)


User = get_user_model()

class PracticeDateDetail(models.Model):
    practice_date = models.ForeignKey(AvailableDate, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_attending = models.BooleanField(default=None, null=True)

    def __str__(self):
        return f"{self.practice_date.name} - {self.user.username}"


