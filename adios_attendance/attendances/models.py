from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

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

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return f"{self.student.name} - {self.date}"

